from __future__ import annotations
import asyncio
import json
import os
import sys
import tempfile
import uuid
from pathlib import Path
from typing import AsyncGenerator

# 将 musicvision/ 根目录加入 sys.path，使 core/visualizers 包可被找到
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

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
    _jobs[job_id] = {"features": features, "audio_path": audio_path}

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
async def export(job_id: str, req: ExportRequest):
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    output_path = str(UPLOAD_DIR / f"{job_id}_viz.{req.format}")
    features: AudioFeatures = job["features"]
    audio_path: str = job["audio_path"]

    loop = asyncio.get_event_loop()
    renderer = CLIRenderer(engine)
    await loop.run_in_executor(
        None, renderer.render, features, audio_path, output_path,
        req.style, req.fps, req.width, req.height
    )
    job["export_path"] = output_path
    return {"status": "done", "download_url": f"/export/{job_id}/download"}


@app.get("/export/{job_id}/download")
async def download(job_id: str):
    job = _jobs.get(job_id)
    if not job or "export_path" not in job:
        raise HTTPException(status_code=404, detail="Export not ready")
    path = job["export_path"]
    filename = Path(path).name
    return FileResponse(path, filename=filename,
                        media_type="application/octet-stream")
