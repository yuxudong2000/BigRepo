from __future__ import annotations
import asyncio
import json
import os
import re
import sys
import tempfile
import uuid
from datetime import datetime
from pathlib import Path
from typing import AsyncGenerator

# 将 musicvision/ 根目录加入 sys.path，使 core/visualizers 包可被找到
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.responses import Response

from core.analyzer import AudioAnalyzer, AudioFeatures
from core.engine import VisualizerEngine
from core.renderer_cli import CLIRenderer

app = FastAPI(title="MusicVision API")
engine = VisualizerEngine()
analyzer = AudioAnalyzer()

# 内存中保存 job 状态
_jobs: dict[str, dict] = {}  # job_id -> {features, audio_path, export_path}

STATIC_DIR = Path(__file__).parent / "static"
UPLOAD_DIR = Path(tempfile.gettempdir()) / "musicvision_uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# 挂载静态文件
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
async def index():
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.get("/plugins")
async def list_plugins():
    return {"plugins": engine.list_plugins()}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix
    audio_path = str(UPLOAD_DIR / f"{uuid.uuid4()}{suffix}")
    with open(audio_path, "wb") as f:
        f.write(await file.read())

    features = analyzer.analyze(audio_path)
    job_id = str(uuid.uuid4())
    # 保存原始文件名（去掉扩展名），用于导出命名
    music_name = Path(file.filename).stem
    _jobs[job_id] = {"features": features, "audio_path": audio_path, "music_name": music_name}

    return {
        "job_id": job_id,
        "bpm": round(features.bpm, 1),
        "key": features.key,
        "duration": round(features.duration, 2),
        "palette": {
            "primary": features.palette.primary,
            "secondary": features.palette.secondary,
            "background": features.palette.background,
            "accent": features.palette.accent,
        },
        "plugins": engine.list_plugins(),
        "n_frames": features.spectrum.shape[1],
    }


async def _frame_generator(job_id: str) -> AsyncGenerator[str, None]:
    """SSE 生成器：逐帧推送频谱和能量数据"""
    job = _jobs.get(job_id)
    if not job:
        yield f"data: {json.dumps({'error': 'job not found'})}\n\n"
        return

    features: AudioFeatures = job["features"]
    n_frames = features.spectrum.shape[1]

    for i in range(n_frames):
        spec_slice = features.spectrum[:64, i].tolist()
        energy_val = float(features.energy[i])

        payload = json.dumps({
            "frame": i,
            "total": n_frames,
            "spectrum": spec_slice,
            "energy": energy_val,
            "beat_times": features.beat_times,
            "bpm": features.bpm,
            "palette": {
                "primary": features.palette.primary,
                "secondary": features.palette.secondary,
                "background": features.palette.background,
                "accent": features.palette.accent,
            },
        })
        yield f"data: {payload}\n\n"
        await asyncio.sleep(0)  # 让出控制权

    yield f"data: {json.dumps({'done': True})}\n\n"


@app.get("/stream/{job_id}")
async def stream(job_id: str):
    if job_id not in _jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return StreamingResponse(
        _frame_generator(job_id),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


class ExportRequest(BaseModel):
    format: str = "mp4"
    style: str = "spectrum"
    fps: int = 30
    width: int = 1920
    height: int = 1080


@app.post("/export/{job_id}")
async def export(job_id: str, req: ExportRequest, background_tasks: BackgroundTasks):
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    music_name = job.get("music_name", "musicvision")
    # 清理文件名中的特殊字符，保留中文、字母、数字、空格、连字符
    safe_name = re.sub(r'[^\w\u4e00-\u9fff\- ]', '', music_name).strip() or "musicvision"
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    export_filename = f"{safe_name}-{timestamp}.{req.format}"
    output_path = str(UPLOAD_DIR / export_filename)
    job["export_filename"] = export_filename
    features: AudioFeatures = job["features"]
    audio_path: str = job["audio_path"]

    # 标记为进行中
    job["export_status"] = "processing"
    job["export_path"] = output_path

    def do_render():
        try:
            renderer = CLIRenderer(engine)
            renderer.render(features, audio_path, output_path,
                            req.style, req.fps, req.width, req.height)
            job["export_status"] = "done"
        except Exception as e:
            job["export_status"] = f"error: {e}"

    background_tasks.add_task(do_render)
    return {"status": "processing", "poll_url": f"/export/{job_id}/status"}


@app.get("/export/{job_id}/status")
async def export_status(job_id: str):
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    status = job.get("export_status", "not_started")
    result = {"status": status}
    if status == "done":
        result["download_url"] = f"/export/{job_id}/download"
    return result


@app.get("/export/{job_id}/download")
async def download(job_id: str):
    job = _jobs.get(job_id)
    if not job or job.get("export_status") != "done":
        raise HTTPException(status_code=404, detail="Export not ready")
    path = job["export_path"]
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    filename = Path(path).name
    # 用 Content-Disposition 头触发浏览器下载
    return FileResponse(
        path,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
