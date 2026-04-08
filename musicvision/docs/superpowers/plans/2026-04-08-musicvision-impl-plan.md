# MusicVision 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**目标：** 实现完整的 MusicVision 音乐可视化工具，支持四种风格、全自动参数推导、Web 实时预览和 MP4/GIF 导出。

**架构：** Python 后端负责音频分析（librosa）和视频导出（moviepy），FastAPI 提供 Web 服务并通过 SSE 向前端推送帧数据，前端 Canvas 2D API 实时渲染可视化效果。可视化风格通过插件系统管理，新增风格只需在 `visualizers/` 目录下添加文件。

**技术栈：** Python 3.10+、librosa、numpy、moviepy、FastAPI、uvicorn、Canvas 2D API、SSE

---

## 文件结构总览

```
musicvision/
├── core/
│   ├── __init__.py
│   ├── analyzer.py          # AudioAnalyzer + AudioFeatures + ColorPalette
│   ├── engine.py            # VisualizerEngine 插件注册与管理
│   └── renderer_cli.py      # CLI 逐帧渲染 + moviepy 合成
├── visualizers/
│   ├── __init__.py
│   ├── base.py              # BaseVisualizer 抽象基类
│   ├── spectrum.py          # 频谱条形
│   ├── waveform.py          # 波形流动
│   ├── particle.py          # 粒子爆炸
│   └── circular.py          # 环形放射
├── web/
│   ├── server.py            # FastAPI 应用 + 所有 API 路由
│   └── static/
│       ├── index.html       # 单页应用 HTML
│       ├── app.js           # 主应用逻辑（上传、SSE、导出）
│       └── canvas-renderer.js  # Canvas 绘制 + 四种风格 JS 实现
├── tests/
│   ├── test_analyzer.py
│   ├── test_engine.py
│   └── test_renderer.py
├── cli.py                   # CLI 入口
├── requirements.txt
└── README.md
```

---

## Task 1：项目基础结构 + 依赖配置

**文件：**
- 创建：`musicvision/requirements.txt`
- 创建：`musicvision/core/__init__.py`
- 创建：`musicvision/visualizers/__init__.py`
- 创建：`musicvision/tests/__init__.py`

- [ ] **Step 1：创建 requirements.txt**

```
librosa>=0.10.0
numpy>=1.24.0
moviepy>=1.0.3
fastapi>=0.110.0
uvicorn>=0.29.0
python-multipart>=0.0.9
pillow>=10.0.0
scipy>=1.11.0
```

- [ ] **Step 2：创建目录和空 `__init__.py`**

```bash
cd musicvision
mkdir -p core visualizers web/static tests
touch core/__init__.py visualizers/__init__.py tests/__init__.py
```

- [ ] **Step 3：安装依赖（确认 ffmpeg 已安装）**

```bash
pip install -r requirements.txt
ffmpeg -version  # 应输出版本号，如未安装：brew install ffmpeg
```

- [ ] **Step 4：提交**

```bash
git add requirements.txt core/__init__.py visualizers/__init__.py tests/__init__.py
git commit -m "chore: 初始化项目结构和依赖配置"
```

---

## Task 2：音频分析器 `core/analyzer.py`

**文件：**
- 创建：`musicvision/core/analyzer.py`
- 创建：`musicvision/tests/test_analyzer.py`

- [ ] **Step 1：先写测试**

```python
# tests/test_analyzer.py
import numpy as np
import pytest
from core.analyzer import AudioAnalyzer, AudioFeatures, ColorPalette

def make_sine_wav(tmp_path, freq=440, duration=3.0, sr=22050):
    """生成一段正弦波并保存为 WAV，用于测试"""
    import scipy.io.wavfile as wav
    t = np.linspace(0, duration, int(sr * duration))
    audio = (np.sin(2 * np.pi * freq * t) * 32767).astype(np.int16)
    path = tmp_path / "test.wav"
    wav.write(str(path), sr, audio)
    return str(path)

def test_audio_features_fields(tmp_path):
    path = make_sine_wav(tmp_path)
    analyzer = AudioAnalyzer()
    features = analyzer.analyze(path)
    assert isinstance(features, AudioFeatures)
    assert features.bpm > 0
    assert features.duration == pytest.approx(3.0, abs=0.1)
    assert features.sample_rate == 22050
    assert features.spectrum.ndim == 2
    assert features.energy.ndim == 1
    assert isinstance(features.palette, ColorPalette)
    assert features.key != ""

def test_palette_fields():
    p = ColorPalette(primary="#00f5ff", secondary="#7b2fff", background="#050510", accent="#ff00aa")
    assert p.primary.startswith("#")
    assert p.background.startswith("#")
```

- [ ] **Step 2：运行测试，确认失败**

```bash
cd musicvision && python -m pytest tests/test_analyzer.py -v
# 预期：ImportError: cannot import name 'AudioAnalyzer'
```

- [ ] **Step 3：实现 `core/analyzer.py`**

```python
from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np
import librosa

@dataclass
class ColorPalette:
    primary: str
    secondary: str
    background: str
    accent: str

@dataclass
class AudioFeatures:
    bpm: float
    beat_times: list[float]
    duration: float
    sample_rate: int
    hop_length: int
    spectrum: np.ndarray      # shape: (n_fft_bins, n_frames)
    energy: np.ndarray        # shape: (n_frames,)
    palette: ColorPalette
    key: str

# 四种预设配色，根据 (高/低能量) × (大/小调) 选择
_PALETTES = {
    ("high", "major"): ColorPalette("#ffaa00", "#ff4400", "#0a0500", "#ffdd00"),
    ("high", "minor"): ColorPalette("#00f5ff", "#7b2fff", "#050510", "#ff00aa"),
    ("low",  "major"): ColorPalette("#00e5aa", "#00b5d8", "#020d0a", "#88ffcc"),
    ("low",  "minor"): ColorPalette("#6644cc", "#220066", "#030008", "#aa66ff"),
}

# 色度轮 —— 检测音调所用
_CHROMA_NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

class AudioAnalyzer:
    def analyze(self, filepath: str, hop_length: int = 512) -> AudioFeatures:
        y, sr = librosa.load(filepath, sr=None, mono=True)
        duration = librosa.get_duration(y=y, sr=sr)

        # BPM & 节拍
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop_length)
        bpm = float(tempo) if np.isscalar(tempo) else float(tempo[0])
        beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=hop_length).tolist()

        # 频谱
        stft = np.abs(librosa.stft(y, hop_length=hop_length))  # (n_fft_bins, n_frames)

        # 能量
        rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]  # (n_frames,)

        # 调式检测
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        key_idx = int(np.argmax(chroma.mean(axis=1)))
        key_note = _CHROMA_NOTES[key_idx]
        # 简单大/小调判断：比较大三度和小三度的色度能量
        major_energy = chroma[(key_idx + 4) % 12].mean()
        minor_energy = chroma[(key_idx + 3) % 12].mean()
        mode = "major" if major_energy >= minor_energy else "minor"
        key = f"{key_note}{'m' if mode == 'minor' else ''}"

        # 配色选择
        avg_energy = float(rms.mean())
        energy_level = "high" if avg_energy > 0.05 else "low"
        palette = _PALETTES[(energy_level, mode)]

        return AudioFeatures(
            bpm=bpm,
            beat_times=beat_times,
            duration=duration,
            sample_rate=sr,
            hop_length=hop_length,
            spectrum=stft,
            energy=rms,
            palette=palette,
            key=key,
        )
```

- [ ] **Step 4：运行测试，确认通过**

```bash
python -m pytest tests/test_analyzer.py -v
# 预期：2 passed
```

- [ ] **Step 5：提交**

```bash
git add core/analyzer.py tests/test_analyzer.py
git commit -m "feat: 实现 AudioAnalyzer — BPM/频谱/能量/配色自动推导"
```

---

## Task 3：可视化引擎 + 抽象基类

**文件：**
- 创建：`musicvision/visualizers/base.py`
- 创建：`musicvision/core/engine.py`
- 创建：`musicvision/tests/test_engine.py`

- [ ] **Step 1：先写测试**

```python
# tests/test_engine.py
import numpy as np
from core.engine import VisualizerEngine
from visualizers.base import BaseVisualizer
from core.analyzer import AudioFeatures, ColorPalette

def _dummy_features() -> AudioFeatures:
    sr = 22050
    hop = 512
    n_frames = 100
    return AudioFeatures(
        bpm=120.0, beat_times=[0.5, 1.0, 1.5],
        duration=3.0, sample_rate=sr, hop_length=hop,
        spectrum=np.random.rand(513, n_frames),
        energy=np.random.rand(n_frames),
        palette=ColorPalette("#00f5ff", "#7b2fff", "#050510", "#ff00aa"),
        key="Am",
    )

def test_engine_lists_builtin_plugins():
    engine = VisualizerEngine()
    plugins = engine.list_plugins()
    assert "spectrum" in plugins
    assert "waveform" in plugins
    assert "particle" in plugins
    assert "circular" in plugins

def test_engine_render_frame_returns_image():
    engine = VisualizerEngine()
    features = _dummy_features()
    frame = engine.render_frame("spectrum", features, frame_idx=0, width=320, height=180)
    assert frame.shape == (180, 320, 3)
    assert frame.dtype == np.uint8
```

- [ ] **Step 2：运行测试，确认失败**

```bash
python -m pytest tests/test_engine.py -v
# 预期：ImportError
```

- [ ] **Step 3：实现 `visualizers/base.py`**

```python
from abc import ABC, abstractmethod
import numpy as np
from core.analyzer import AudioFeatures

class BaseVisualizer(ABC):
    name: str        # 唯一标识符，如 "spectrum"
    display_name: str  # 展示名称，如 "频谱条形"

    @abstractmethod
    def render_frame(self, features: AudioFeatures, frame_idx: int,
                     width: int, height: int) -> np.ndarray:
        """渲染单帧，返回 shape=(height, width, 3) 的 uint8 BGR 图像"""
```

- [ ] **Step 4：实现 `core/engine.py`**

```python
from __future__ import annotations
import importlib
import pkgutil
import visualizers
from visualizers.base import BaseVisualizer
from core.analyzer import AudioFeatures
import numpy as np

class VisualizerEngine:
    def __init__(self):
        self._registry: dict[str, BaseVisualizer] = {}
        self._auto_discover()

    def _auto_discover(self):
        """扫描 visualizers/ 包，自动注册所有 BaseVisualizer 子类"""
        for finder, module_name, _ in pkgutil.iter_modules(visualizers.__path__):
            if module_name == "base":
                continue
            module = importlib.import_module(f"visualizers.{module_name}")
            for attr_name in dir(module):
                obj = getattr(module, attr_name)
                if (isinstance(obj, type)
                        and issubclass(obj, BaseVisualizer)
                        and obj is not BaseVisualizer
                        and hasattr(obj, "name")):
                    instance = obj()
                    self._registry[instance.name] = instance

    def list_plugins(self) -> list[str]:
        return list(self._registry.keys())

    def render_frame(self, style: str, features: AudioFeatures,
                     frame_idx: int, width: int = 1920, height: int = 1080) -> np.ndarray:
        if style not in self._registry:
            raise ValueError(f"未知风格: {style}，可用: {self.list_plugins()}")
        return self._registry[style].render_frame(features, frame_idx, width, height)
```

- [ ] **Step 5：创建最简 `visualizers/spectrum.py`（让测试通过）**

```python
import numpy as np
from visualizers.base import BaseVisualizer
from core.analyzer import AudioFeatures

class SpectrumVisualizer(BaseVisualizer):
    name = "spectrum"
    display_name = "频谱条形"

    def render_frame(self, features: AudioFeatures, frame_idx: int,
                     width: int, height: int) -> np.ndarray:
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        return frame  # 占位，Task 5 实现完整效果
```

对 `waveform.py`、`particle.py`、`circular.py` 执行相同的占位结构（name 不同即可）。

- [ ] **Step 6：运行测试，确认通过**

```bash
python -m pytest tests/test_engine.py -v
# 预期：2 passed
```

- [ ] **Step 7：提交**

```bash
git add visualizers/base.py core/engine.py visualizers/spectrum.py visualizers/waveform.py visualizers/particle.py visualizers/circular.py tests/test_engine.py
git commit -m "feat: 实现 VisualizerEngine 插件系统 + BaseVisualizer 基类"
```

---

## Task 4：CLI 渲染器 `core/renderer_cli.py` + `cli.py`

**文件：**
- 创建：`musicvision/core/renderer_cli.py`
- 创建：`musicvision/cli.py`
- 创建：`musicvision/tests/test_renderer.py`

- [ ] **Step 1：先写测试**

```python
# tests/test_renderer.py
import numpy as np
import pytest
from core.analyzer import AudioFeatures, ColorPalette
from core.engine import VisualizerEngine
from core.renderer_cli import CLIRenderer

def _dummy_features() -> AudioFeatures:
    sr = 22050
    hop = 512
    n_frames = 50
    return AudioFeatures(
        bpm=120.0, beat_times=[0.5, 1.0],
        duration=1.0, sample_rate=sr, hop_length=hop,
        spectrum=np.random.rand(513, n_frames),
        energy=np.random.rand(n_frames),
        palette=ColorPalette("#00f5ff", "#7b2fff", "#050510", "#ff00aa"),
        key="Am",
    )

def test_renderer_creates_mp4(tmp_path):
    import scipy.io.wavfile as wav
    # 生成 1 秒音频
    sr = 22050
    audio = (np.sin(2 * np.pi * 440 * np.linspace(0, 1, sr)) * 32767).astype(np.int16)
    audio_path = str(tmp_path / "input.wav")
    wav.write(audio_path, sr, audio)

    output_path = str(tmp_path / "output.mp4")
    features = _dummy_features()
    engine = VisualizerEngine()
    renderer = CLIRenderer(engine)
    renderer.render(features, audio_path, output_path, style="spectrum",
                    fps=10, width=320, height=180)

    assert (tmp_path / "output.mp4").exists()
    assert (tmp_path / "output.mp4").stat().st_size > 0
```

- [ ] **Step 2：运行测试，确认失败**

```bash
python -m pytest tests/test_renderer.py -v
# 预期：ImportError: cannot import name 'CLIRenderer'
```

- [ ] **Step 3：实现 `core/renderer_cli.py`**

```python
from __future__ import annotations
import numpy as np
from moviepy.editor import ImageSequenceClip, AudioFileClip
from core.analyzer import AudioFeatures
from core.engine import VisualizerEngine

class CLIRenderer:
    def __init__(self, engine: VisualizerEngine):
        self.engine = engine

    def render(self, features: AudioFeatures, audio_path: str,
               output_path: str, style: str = "spectrum",
               fps: int = 30, width: int = 1920, height: int = 1080) -> None:
        """逐帧渲染并导出 MP4 或 GIF"""
        total_frames = int(features.duration * fps)
        # 每帧对应 AudioFeatures 中的帧索引（spectrum 的时间轴）
        feature_frames = features.spectrum.shape[1]

        frames: list[np.ndarray] = []
        for i in range(total_frames):
            # 将视频帧映射到 spectrum 帧索引
            feature_idx = int(i / total_frames * feature_frames)
            feature_idx = min(feature_idx, feature_frames - 1)
            bgr = self.engine.render_frame(style, features, feature_idx, width, height)
            # moviepy 需要 RGB
            rgb = bgr[:, :, ::-1]
            frames.append(rgb)

        clip = ImageSequenceClip(frames, fps=fps)
        audio = AudioFileClip(audio_path).subclip(0, features.duration)
        clip = clip.set_audio(audio)

        if output_path.endswith(".gif"):
            clip.write_gif(output_path, fps=fps)
        else:
            clip.write_videofile(output_path, fps=fps, codec="libx264",
                                 audio_codec="aac", logger=None)
```

- [ ] **Step 4：实现 `cli.py`**

```python
#!/usr/bin/env python3
"""MusicVision CLI — 音乐可视化视频生成工具"""
import argparse
import os
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="MusicVision: 音乐 → 可视化视频")
    parser.add_argument("audio", help="音频文件路径（MP3/WAV/FLAC/OGG）")
    parser.add_argument("--style", default="auto",
                        choices=["auto", "spectrum", "waveform", "particle", "circular"],
                        help="可视化风格（默认 auto：自动选择）")
    parser.add_argument("--output", default=None, help="输出文件路径（默认：<input>_viz.mp4）")
    parser.add_argument("--format", default="mp4", choices=["mp4", "gif"])
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    args = parser.parse_args()

    # 延迟导入，避免慢速导入影响 --help 响应
    from core.analyzer import AudioAnalyzer
    from core.engine import VisualizerEngine
    from core.renderer_cli import CLIRenderer

    if not os.path.exists(args.audio):
        print(f"错误：找不到文件 {args.audio}", file=sys.stderr)
        sys.exit(1)

    output = args.output or str(Path(args.audio).stem + f"_viz.{args.format}")

    print(f"🎵 正在分析音频: {args.audio}")
    analyzer = AudioAnalyzer()
    features = analyzer.analyze(args.audio)
    print(f"   BPM: {features.bpm:.1f} | 调: {features.key} | 时长: {features.duration:.1f}s")

    style = args.style
    if style == "auto":
        # 高能量 → particle；低能量 → waveform；默认 spectrum
        avg = float(features.energy.mean())
        style = "particle" if avg > 0.1 else ("waveform" if avg < 0.03 else "spectrum")
        print(f"   自动选择风格: {style}")

    engine = VisualizerEngine()
    renderer = CLIRenderer(engine)
    print(f"🎨 开始渲染 ({args.width}x{args.height} @ {args.fps}fps)...")
    renderer.render(features, args.audio, output,
                    style=style, fps=args.fps, width=args.width, height=args.height)
    print(f"✅ 已导出: {output}")

if __name__ == "__main__":
    main()
```

- [ ] **Step 5：运行测试**

```bash
python -m pytest tests/test_renderer.py -v
# 预期：1 passed（耗时约 10-30 秒）
```

- [ ] **Step 6：提交**

```bash
git add core/renderer_cli.py cli.py tests/test_renderer.py
git commit -m "feat: 实现 CLIRenderer + cli.py 入口"
```

---

## Task 5：四种可视化风格完整实现

**文件：**
- 修改：`musicvision/visualizers/spectrum.py`
- 修改：`musicvision/visualizers/waveform.py`
- 修改：`musicvision/visualizers/particle.py`
- 修改：`musicvision/visualizers/circular.py`

- [ ] **Step 1：实现 `visualizers/spectrum.py` — 频谱条形**

```python
import numpy as np
import cv2
from visualizers.base import BaseVisualizer
from core.analyzer import AudioFeatures

def _hex_to_bgr(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (b, g, r)

class SpectrumVisualizer(BaseVisualizer):
    name = "spectrum"
    display_name = "频谱条形"

    def render_frame(self, features: AudioFeatures, frame_idx: int,
                     width: int, height: int) -> np.ndarray:
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        palette = features.palette

        # 取当前帧频谱（前 128 个 bin，对应人耳可听范围）
        spec = features.spectrum[:128, frame_idx]
        spec = spec / (spec.max() + 1e-8)  # 归一化到 [0, 1]

        n_bars = 64
        bar_w = width // n_bars
        # 能量归一化，用于控制发光强度
        energy = float(features.energy[frame_idx]) / (features.energy.max() + 1e-8)

        # 降采样到 n_bars
        indices = np.linspace(0, len(spec) - 1, n_bars).astype(int)
        magnitudes = spec[indices]

        color_start = _hex_to_bgr(palette.primary)
        color_end = _hex_to_bgr(palette.accent)

        for i, mag in enumerate(magnitudes):
            bar_h = int(mag * height * 0.85)
            if bar_h < 2:
                continue
            x1 = i * bar_w + 1
            x2 = x1 + bar_w - 2
            y1 = height - bar_h
            y2 = height

            # 线性插值颜色（低频→primary，高频→accent）
            t = i / n_bars
            color = tuple(int(color_start[c] * (1 - t) + color_end[c] * t) for c in range(3))
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)

            # 顶部发光点（节拍时更亮）
            glow_intensity = int(200 + 55 * energy)
            glow_color = tuple(min(255, int(c * 1.5)) for c in color)
            cv2.rectangle(frame, (x1, y1), (x2, y1 + 3), glow_color, -1)

        return frame
```

- [ ] **Step 2：实现 `visualizers/waveform.py` — 波形流动**

```python
import numpy as np
import cv2
from visualizers.base import BaseVisualizer
from core.analyzer import AudioFeatures

def _hex_to_bgr(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (b, g, r)

class WaveformVisualizer(BaseVisualizer):
    name = "waveform"
    display_name = "波形流动"

    def render_frame(self, features: AudioFeatures, frame_idx: int,
                     width: int, height: int) -> np.ndarray:
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        palette = features.palette

        # 取当前帧附近若干帧的频谱均值作为波形
        window = 4
        start = max(0, frame_idx - window)
        end = min(features.spectrum.shape[1], frame_idx + window + 1)
        spec = features.spectrum[:, start:end].mean(axis=1)

        # 降采样到 width 个点
        indices = np.linspace(0, len(spec) - 1, width).astype(int)
        wave = spec[indices]
        wave = wave / (wave.max() + 1e-8)

        energy = float(features.energy[frame_idx]) / (features.energy.max() + 1e-8)
        center_y = height // 2

        color_a = _hex_to_bgr(palette.primary)
        color_b = _hex_to_bgr(palette.secondary)

        points = []
        for x in range(width):
            y = int(center_y - wave[x] * center_y * 0.8)
            points.append((x, y))

        # 绘制渐变折线（分段绘制以实现渐变色）
        segment = max(1, width // 64)
        for i in range(0, width - segment, segment):
            t = i / width
            color = tuple(int(color_a[c] * (1 - t) + color_b[c] * t) for c in range(3))
            thickness = 2 + int(energy * 3)
            cv2.line(frame, points[i], points[i + segment], color, thickness, cv2.LINE_AA)

        # 镜像下半部分（对称波形）
        for x in range(width):
            y_top = points[x][1]
            y_bot = height - (center_y - y_top) - 1
            if 0 <= y_bot < height:
                t = x / width
                color = tuple(int(color_a[c] * (1 - t) + color_b[c] * t) for c in range(3))
                frame[y_bot, x] = [c // 2 for c in color]  # 下半透明

        return frame
```

- [ ] **Step 3：实现 `visualizers/particle.py` — 粒子爆炸**

```python
import numpy as np
import cv2
from visualizers.base import BaseVisualizer
from core.analyzer import AudioFeatures

def _hex_to_bgr(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (b, g, r)

class ParticleVisualizer(BaseVisualizer):
    name = "particle"
    display_name = "粒子爆炸"

    def render_frame(self, features: AudioFeatures, frame_idx: int,
                     width: int, height: int) -> np.ndarray:
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        palette = features.palette
        rng = np.random.default_rng(frame_idx)  # 固定种子保证可复现

        energy = float(features.energy[frame_idx]) / (features.energy.max() + 1e-8)
        # 检测当前帧是否为节拍帧
        fps_approx = features.spectrum.shape[1] / features.duration
        beat_frames = set(int(t * fps_approx) for t in features.beat_times)
        is_beat = frame_idx in beat_frames

        cx, cy = width // 2, height // 2
        n_particles = int(200 + energy * 600 + (400 if is_beat else 0))

        colors = [
            _hex_to_bgr(palette.primary),
            _hex_to_bgr(palette.secondary),
            _hex_to_bgr(palette.accent),
        ]

        for _ in range(n_particles):
            angle = rng.uniform(0, 2 * np.pi)
            # 节拍时粒子飞得更远
            max_r = (0.6 if is_beat else 0.35) * min(width, height)
            radius = rng.uniform(0, max_r) * (0.3 + 0.7 * energy)
            px = int(cx + radius * np.cos(angle))
            py = int(cy + radius * np.sin(angle))

            if not (0 <= px < width and 0 <= py < height):
                continue

            color = colors[rng.integers(len(colors))]
            size = rng.integers(1, 5 if is_beat else 3)
            brightness = 0.4 + 0.6 * energy
            draw_color = tuple(int(c * brightness) for c in color)
            cv2.circle(frame, (px, py), size, draw_color, -1)

        # 中心发光核心
        glow_r = int(20 + energy * 40 + (30 if is_beat else 0))
        core_color = _hex_to_bgr(palette.primary)
        cv2.circle(frame, (cx, cy), glow_r, core_color, -1)
        cv2.circle(frame, (cx, cy), glow_r // 2, (255, 255, 255), -1)

        return frame
```

- [ ] **Step 4：实现 `visualizers/circular.py` — 环形放射**

```python
import numpy as np
import cv2
from visualizers.base import BaseVisualizer
from core.analyzer import AudioFeatures

def _hex_to_bgr(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (b, g, r)

class CircularVisualizer(BaseVisualizer):
    name = "circular"
    display_name = "环形放射"

    def render_frame(self, features: AudioFeatures, frame_idx: int,
                     width: int, height: int) -> np.ndarray:
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        palette = features.palette

        spec = features.spectrum[:64, frame_idx]
        spec = spec / (spec.max() + 1e-8)
        energy = float(features.energy[frame_idx]) / (features.energy.max() + 1e-8)

        cx, cy = width // 2, height // 2
        base_r = int(min(width, height) * 0.15)  # 内圆半径
        max_bar = int(min(width, height) * 0.35)  # 最大条长

        n_bars = 64
        indices = np.linspace(0, len(spec) - 1, n_bars).astype(int)
        magnitudes = spec[indices]

        # 旋转角度：随时间 + BPM 驱动
        rotation = (frame_idx / features.spectrum.shape[1]) * features.bpm / 60 * 2 * np.pi

        color_a = _hex_to_bgr(palette.primary)
        color_b = _hex_to_bgr(palette.secondary)

        for i, mag in enumerate(magnitudes):
            angle = rotation + (2 * np.pi * i / n_bars)
            bar_len = int(mag * max_bar)
            if bar_len < 2:
                continue

            x1 = int(cx + base_r * np.cos(angle))
            y1 = int(cy + base_r * np.sin(angle))
            x2 = int(cx + (base_r + bar_len) * np.cos(angle))
            y2 = int(cy + (base_r + bar_len) * np.sin(angle))

            t = i / n_bars
            color = tuple(int(color_a[c] * (1 - t) + color_b[c] * t) for c in range(3))
            thickness = max(1, int(2 + energy * 3))
            cv2.line(frame, (x1, y1), (x2, y2), color, thickness, cv2.LINE_AA)

        # 内圆
        inner_color = _hex_to_bgr(palette.accent)
        cv2.circle(frame, (cx, cy), base_r, inner_color, 2)
        cv2.circle(frame, (cx, cy), int(base_r * 0.4), inner_color, -1)

        return frame
```

- [ ] **Step 5：快速可视性验证（可选，需要一段音频文件）**

```bash
python cli.py path/to/song.mp3 --style spectrum --fps 5 --width 640 --height 360 --output test_spectrum.mp4
python cli.py path/to/song.mp3 --style particle --fps 5 --width 640 --height 360 --output test_particle.mp4
```

- [ ] **Step 6：运行全部测试**

```bash
python -m pytest tests/ -v
# 预期：全部通过
```

- [ ] **Step 7：提交**

```bash
git add visualizers/spectrum.py visualizers/waveform.py visualizers/particle.py visualizers/circular.py
git commit -m "feat: 实现四种完整可视化风格 — 频谱/波形/粒子/环形"
```

---

## Task 6：FastAPI Web 服务 `web/server.py`

**文件：**
- 创建：`musicvision/web/server.py`

- [ ] **Step 1：实现 `web/server.py`**

```python
from __future__ import annotations
import asyncio
import io
import json
import os
import tempfile
import uuid
from pathlib import Path
from typing import AsyncGenerator

import numpy as np
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

# 挂载静态文件（index.html 等）
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
async def index():
    return FileResponse(str(STATIC_DIR / "index.html"))

@app.get("/plugins")
async def list_plugins():
    return {"plugins": engine.list_plugins()}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # 保存上传文件
    suffix = Path(file.filename).suffix
    audio_path = str(UPLOAD_DIR / f"{uuid.uuid4()}{suffix}")
    with open(audio_path, "wb") as f:
        f.write(await file.read())

    # 分析
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

async def _frame_generator(job_id: str, style: str) -> AsyncGenerator[str, None]:
    """SSE 生成器：逐帧推送频谱和能量数据"""
    job = _jobs.get(job_id)
    if not job:
        yield f"data: {json.dumps({'error': 'job not found'})}\n\n"
        return

    features: AudioFeatures = job["features"]
    n_frames = features.spectrum.shape[1]

    for i in range(n_frames):
        spec_slice = features.spectrum[:64, i].tolist()  # 前64个bin
        energy_val = float(features.energy[i])
        beat_times = features.beat_times

        payload = json.dumps({
            "frame": i,
            "total": n_frames,
            "spectrum": spec_slice,
            "energy": energy_val,
            "beat_times": beat_times,
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
async def stream(job_id: str, style: str = "spectrum"):
    if job_id not in _jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return StreamingResponse(
        _frame_generator(job_id, style),
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

    # 后台异步导出
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
```

- [ ] **Step 2：提交**

```bash
git add web/server.py
git commit -m "feat: 实现 FastAPI Web 服务 — analyze/stream/export API"
```

---

## Task 7：前端 — `index.html` + `app.js` + `canvas-renderer.js`

**文件：**
- 创建：`musicvision/web/static/index.html`
- 创建：`musicvision/web/static/app.js`
- 创建：`musicvision/web/static/canvas-renderer.js`

- [ ] **Step 1：创建 `index.html`**

```html
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MusicVision</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #050510; color: #e0e0e0; font-family: system-ui, sans-serif; height: 100vh; display: flex; flex-direction: column; }
    header { background: #0d0d2a; padding: 10px 16px; border-bottom: 1px solid #1a1a3a; display: flex; align-items: center; }
    header h1 { font-size: 16px; color: #7b2fff; }
    .main { display: flex; flex: 1; overflow: hidden; }

    /* 左侧面板 */
    #sidebar { width: 180px; background: #0d0d2a; border-right: 1px solid #1a1a3a; padding: 14px; display: flex; flex-direction: column; gap: 12px; overflow-y: auto; }
    .sidebar-section h3 { font-size: 10px; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
    .style-btn { width: 100%; padding: 7px 10px; background: #1a1a3a; border: none; border-radius: 4px; color: #aaa; font-size: 12px; cursor: pointer; text-align: left; margin-bottom: 4px; }
    .style-btn.active { background: #7b2fff; color: #fff; }
    #drop-zone { border: 1px dashed #7b2fff; border-radius: 6px; padding: 16px 8px; text-align: center; color: #7b2fff; font-size: 12px; cursor: pointer; }
    #drop-zone:hover, #drop-zone.dragover { background: #7b2fff22; }
    #file-input { display: none; }
    .info-row { font-size: 11px; color: #aaa; display: flex; justify-content: space-between; }
    .info-row span:last-child { color: #00f5ff; }
    .energy-bar { height: 4px; background: #1a1a3a; border-radius: 2px; margin-top: 2px; }
    .energy-fill { height: 100%; background: linear-gradient(to right, #7b2fff, #ff00aa); border-radius: 2px; transition: width 0.1s; }
    .export-btn { width: 100%; padding: 8px; border: none; border-radius: 4px; font-size: 12px; cursor: pointer; }
    .export-btn.mp4 { background: #1a3a1a; color: #00ff88; }
    .export-btn.gif { background: #1a1a3a; color: #aaa; }
    .export-btn:disabled { opacity: 0.4; cursor: not-allowed; }
    #status { font-size: 11px; color: #555; text-align: center; }

    /* 右侧 canvas 区 */
    #canvas-area { flex: 1; display: flex; flex-direction: column; background: #050510; }
    #viz-canvas { flex: 1; width: 100%; display: block; }

    /* 播放控制条 */
    #transport { background: #0d0d2a; border-top: 1px solid #1a1a3a; padding: 8px 16px; display: flex; align-items: center; gap: 12px; }
    .transport-btn { background: none; border: none; color: #aaa; font-size: 20px; cursor: pointer; }
    .transport-btn:hover { color: #fff; }
    #progress-bar { flex: 1; height: 3px; background: #1a1a3a; border-radius: 2px; cursor: pointer; }
    #progress-fill { height: 100%; background: linear-gradient(to right, #7b2fff, #ff00aa); border-radius: 2px; width: 0%; }
    #time-display { font-size: 11px; color: #555; min-width: 70px; text-align: right; }
  </style>
</head>
<body>
  <header><h1>🎵 MusicVision</h1></header>
  <div class="main">
    <div id="sidebar">
      <div class="sidebar-section">
        <h3>可视化风格</h3>
        <button class="style-btn active" data-style="spectrum">■ 频谱条形</button>
        <button class="style-btn" data-style="waveform">≋ 波形流动</button>
        <button class="style-btn" data-style="particle">✦ 粒子爆炸</button>
        <button class="style-btn" data-style="circular">◎ 环形放射</button>
      </div>
      <div class="sidebar-section">
        <h3>音乐文件</h3>
        <div id="drop-zone">
          + 拖拽 / 点击<br>选择音乐文件
          <input type="file" id="file-input" accept=".mp3,.wav,.flac,.ogg">
        </div>
      </div>
      <div class="sidebar-section" id="info-section" style="display:none">
        <h3>音乐信息</h3>
        <div class="info-row"><span>BPM</span><span id="info-bpm">—</span></div>
        <div class="info-row"><span>调</span><span id="info-key">—</span></div>
        <div class="info-row"><span>时长</span><span id="info-dur">—</span></div>
        <div class="info-row"><span>能量</span></div>
        <div class="energy-bar"><div class="energy-fill" id="energy-fill" style="width:0%"></div></div>
      </div>
      <div class="sidebar-section">
        <h3>导出</h3>
        <button class="export-btn mp4" id="btn-export-mp4" disabled>⬇ 导出 MP4</button>
        <button class="export-btn gif" id="btn-export-gif" disabled>⬇ 导出 GIF</button>
      </div>
      <div id="status">等待上传文件...</div>
    </div>
    <div id="canvas-area">
      <canvas id="viz-canvas"></canvas>
      <div id="transport">
        <button class="transport-btn" id="btn-prev">⏮</button>
        <button class="transport-btn" id="btn-play">▶</button>
        <button class="transport-btn" id="btn-next">⏭</button>
        <div id="progress-bar"><div id="progress-fill"></div></div>
        <span id="time-display">0:00 / 0:00</span>
      </div>
    </div>
  </div>
  <script src="/static/canvas-renderer.js"></script>
  <script src="/static/app.js"></script>
</body>
</html>
```

- [ ] **Step 2：创建 `canvas-renderer.js` — 四种风格的 JS 渲染实现**

```javascript
// canvas-renderer.js — Canvas 2D 渲染四种可视化风格

function hexToBgr(hex) {
  const h = hex.replace('#', '');
  return [parseInt(h.slice(4,6),16), parseInt(h.slice(2,4),16), parseInt(h.slice(0,2),16)];
}
function hexToRgb(hex) {
  const h = hex.replace('#', '');
  return [parseInt(h.slice(0,2),16), parseInt(h.slice(2,4),16), parseInt(h.slice(4,6),16)];
}

const Renderers = {
  spectrum(ctx, w, h, frameData) {
    const { spectrum, energy, palette } = frameData;
    ctx.fillStyle = palette.background;
    ctx.fillRect(0, 0, w, h);

    const n = Math.min(spectrum.length, 64);
    const barW = w / n;
    const maxE = frameData.maxEnergy || 0.1;
    const energyNorm = Math.min(energy / maxE, 1);

    for (let i = 0; i < n; i++) {
      const mag = spectrum[i] / (Math.max(...spectrum.slice(0,64)) + 1e-8);
      const barH = mag * h * 0.85;
      const t = i / n;
      const r1 = hexToRgb(palette.primary), r2 = hexToRgb(palette.accent);
      const r = Math.round(r1[0]*(1-t) + r2[0]*t);
      const g = Math.round(r1[1]*(1-t) + r2[1]*t);
      const b = Math.round(r1[2]*(1-t) + r2[2]*t);
      ctx.fillStyle = `rgb(${r},${g},${b})`;
      ctx.fillRect(i*barW + 1, h - barH, barW - 2, barH);
      // 顶部发光
      ctx.fillStyle = `rgba(${Math.min(255,r*1.5|0)},${Math.min(255,g*1.5|0)},${Math.min(255,b*1.5|0)},${0.6 + 0.4*energyNorm})`;
      ctx.fillRect(i*barW + 1, h - barH, barW - 2, 3);
    }
  },

  waveform(ctx, w, h, frameData) {
    const { spectrum, energy, palette } = frameData;
    ctx.fillStyle = palette.background;
    ctx.fillRect(0, 0, w, h);

    const maxSpec = Math.max(...spectrum) + 1e-8;
    const cy = h / 2;
    const r1 = hexToRgb(palette.primary), r2 = hexToRgb(palette.secondary);

    ctx.lineWidth = 2 + energy * 10;
    ctx.lineJoin = 'round';

    // 上半波形
    ctx.beginPath();
    for (let x = 0; x < w; x++) {
      const idx = Math.floor(x / w * spectrum.length);
      const mag = spectrum[idx] / maxSpec;
      const y = cy - mag * cy * 0.8;
      const t = x / w;
      if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    const grad = ctx.createLinearGradient(0, 0, w, 0);
    grad.addColorStop(0, palette.primary);
    grad.addColorStop(1, palette.secondary);
    ctx.strokeStyle = grad;
    ctx.stroke();

    // 下半镜像（半透明）
    ctx.globalAlpha = 0.3;
    ctx.beginPath();
    for (let x = 0; x < w; x++) {
      const idx = Math.floor(x / w * spectrum.length);
      const mag = spectrum[idx] / maxSpec;
      const y = cy + mag * cy * 0.8;
      if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
    ctx.globalAlpha = 1;
  },

  particle(ctx, w, h, frameData) {
    const { spectrum, energy, palette, frame, bpm, beat_times, total } = frameData;
    ctx.fillStyle = palette.background;
    ctx.fillRect(0, 0, w, h);

    const maxE = frameData.maxEnergy || 0.1;
    const energyNorm = Math.min(energy / maxE, 1);
    const fps = total / frameData.duration;
    const isBeat = beat_times.some(t => Math.abs(t * fps - frame) < 1.5);

    const cx = w/2, cy = h/2;
    const nParticles = Math.floor(200 + energyNorm * 600 + (isBeat ? 400 : 0));
    const colors = [palette.primary, palette.secondary, palette.accent].map(hexToRgb);

    // 固定随机种子（用 frame 作为种子的简单模拟）
    const rng = mulberry32(frame * 1234567);
    for (let i = 0; i < nParticles; i++) {
      const angle = rng() * Math.PI * 2;
      const maxR = (isBeat ? 0.6 : 0.35) * Math.min(w, h);
      const radius = rng() * maxR * (0.3 + 0.7 * energyNorm);
      const px = cx + radius * Math.cos(angle);
      const py = cy + radius * Math.sin(angle);
      const color = colors[Math.floor(rng() * colors.length)];
      const size = 1 + rng() * (isBeat ? 4 : 2);
      const bright = 0.4 + 0.6 * energyNorm;
      ctx.fillStyle = `rgba(${color[0]*bright|0},${color[1]*bright|0},${color[2]*bright|0},0.9)`;
      ctx.beginPath();
      ctx.arc(px, py, size, 0, Math.PI*2);
      ctx.fill();
    }
    // 中心核心
    const gR = 20 + energyNorm * 40 + (isBeat ? 30 : 0);
    const c = hexToRgb(palette.primary);
    const grd = ctx.createRadialGradient(cx,cy,0, cx,cy,gR);
    grd.addColorStop(0, '#ffffff');
    grd.addColorStop(0.4, `rgb(${c[0]},${c[1]},${c[2]})`);
    grd.addColorStop(1, 'transparent');
    ctx.fillStyle = grd;
    ctx.beginPath(); ctx.arc(cx, cy, gR, 0, Math.PI*2); ctx.fill();
  },

  circular(ctx, w, h, frameData) {
    const { spectrum, energy, palette, frame, total, bpm } = frameData;
    ctx.fillStyle = palette.background;
    ctx.fillRect(0, 0, w, h);

    const maxSpec = Math.max(...spectrum) + 1e-8;
    const maxE = frameData.maxEnergy || 0.1;
    const energyNorm = Math.min(energy / maxE, 1);
    const cx = w/2, cy = h/2;
    const baseR = Math.min(w,h) * 0.15;
    const maxBar = Math.min(w,h) * 0.35;
    const rotation = (frame / total) * (bpm / 60) * Math.PI * 2;

    const n = Math.min(spectrum.length, 64);
    const r1 = hexToRgb(palette.primary), r2 = hexToRgb(palette.secondary);

    ctx.lineWidth = Math.max(1, 2 + energyNorm * 3);

    for (let i = 0; i < n; i++) {
      const mag = spectrum[i] / maxSpec;
      const barLen = mag * maxBar;
      const angle = rotation + (2 * Math.PI * i / n);
      const x1 = cx + baseR * Math.cos(angle);
      const y1 = cy + baseR * Math.sin(angle);
      const x2 = cx + (baseR + barLen) * Math.cos(angle);
      const y2 = cy + (baseR + barLen) * Math.sin(angle);
      const t = i / n;
      const r = Math.round(r1[0]*(1-t) + r2[0]*t);
      const g = Math.round(r1[1]*(1-t) + r2[1]*t);
      const b = Math.round(r1[2]*(1-t) + r2[2]*t);
      ctx.strokeStyle = `rgb(${r},${g},${b})`;
      ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke();
    }
    // 内圆
    const ac = hexToRgb(palette.accent);
    ctx.strokeStyle = `rgb(${ac[0]},${ac[1]},${ac[2]})`;
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(cx,cy,baseR,0,Math.PI*2); ctx.stroke();
    ctx.fillStyle = `rgba(${ac[0]},${ac[1]},${ac[2]},0.8)`;
    ctx.beginPath(); ctx.arc(cx,cy,baseR*0.4,0,Math.PI*2); ctx.fill();
  }
};

// 简单的固定种子随机数生成器（mulberry32）
function mulberry32(a) {
  return function() {
    a |= 0; a = a + 0x6D2B79F5 | 0;
    let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
```

- [ ] **Step 3：创建 `app.js` — 主应用逻辑**

```javascript
// app.js — MusicVision 前端主逻辑

const canvas = document.getElementById('viz-canvas');
const ctx = canvas.getContext('2d');
let jobId = null, currentStyle = 'spectrum', isPlaying = false;
let frames = [], maxEnergy = 0.1, currentFrame = 0, animationId = null;
let audioInfo = {};

// 自适应 canvas 尺寸
function resizeCanvas() {
  const area = document.getElementById('canvas-area');
  canvas.width = area.clientWidth;
  canvas.height = area.clientHeight - document.getElementById('transport').offsetHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// 风格切换
document.querySelectorAll('.style-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.style-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentStyle = btn.dataset.style;
  });
});

// 文件上传
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('dragover'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', e => {
  e.preventDefault(); dropZone.classList.remove('dragover');
  if (e.dataTransfer.files[0]) uploadFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener('change', () => { if (fileInput.files[0]) uploadFile(fileInput.files[0]); });

async function uploadFile(file) {
  setStatus('正在分析音频...');
  const form = new FormData();
  form.append('file', file);
  const res = await fetch('/analyze', { method: 'POST', body: form });
  const data = await res.json();
  jobId = data.job_id;
  audioInfo = data;
  document.getElementById('info-bpm').textContent = data.bpm;
  document.getElementById('info-key').textContent = data.key;
  document.getElementById('info-dur').textContent = formatTime(data.duration);
  document.getElementById('info-section').style.display = 'block';
  document.getElementById('btn-export-mp4').disabled = false;
  document.getElementById('btn-export-gif').disabled = false;
  setStatus('正在加载帧数据...');
  await loadFrames(jobId, currentStyle);
  setStatus('就绪');
  startPlayback();
}

async function loadFrames(jId, style) {
  frames = [];
  const evtSource = new EventSource(`/stream/${jId}?style=${style}`);
  return new Promise((resolve) => {
    evtSource.onmessage = (e) => {
      const d = JSON.parse(e.data);
      if (d.done) { evtSource.close(); resolve(); return; }
      frames.push(d);
      maxEnergy = Math.max(maxEnergy, d.energy);
    };
    evtSource.onerror = () => { evtSource.close(); resolve(); };
  });
}

function startPlayback() {
  isPlaying = true;
  document.getElementById('btn-play').textContent = '⏸';
  playLoop();
}

function playLoop() {
  if (!isPlaying || frames.length === 0) return;
  const frameData = { ...frames[currentFrame], maxEnergy, duration: audioInfo.duration };
  resizeCanvas();
  if (Renderers[currentStyle]) {
    Renderers[currentStyle](ctx, canvas.width, canvas.height, frameData);
  }
  // 更新能量条
  const e = frameData.energy / maxEnergy;
  document.getElementById('energy-fill').style.width = (e * 100) + '%';
  // 更新进度
  document.getElementById('progress-fill').style.width = (currentFrame / frames.length * 100) + '%';
  document.getElementById('time-display').textContent =
    `${formatTime(frameData.frame / frames.length * audioInfo.duration)} / ${formatTime(audioInfo.duration)}`;
  currentFrame = (currentFrame + 1) % frames.length;
  // 约 30fps
  animationId = setTimeout(playLoop, 1000 / 30);
}

// 播放控制
document.getElementById('btn-play').addEventListener('click', () => {
  isPlaying = !isPlaying;
  document.getElementById('btn-play').textContent = isPlaying ? '⏸' : '▶';
  if (isPlaying) playLoop();
  else clearTimeout(animationId);
});
document.getElementById('btn-prev').addEventListener('click', () => { currentFrame = 0; });
document.getElementById('btn-next').addEventListener('click', () => { currentFrame = frames.length - 1; });

// 导出
async function doExport(format) {
  if (!jobId) return;
  setStatus(`导出 ${format.toUpperCase()} 中...`);
  document.getElementById('btn-export-mp4').disabled = true;
  document.getElementById('btn-export-gif').disabled = true;
  const res = await fetch(`/export/${jobId}`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ format, style: currentStyle, fps: 30, width: 1920, height: 1080 }),
  });
  const data = await res.json();
  if (data.download_url) {
    const a = document.createElement('a');
    a.href = data.download_url; a.download = `musicvision.${format}`; a.click();
    setStatus('导出完成！');
  }
  document.getElementById('btn-export-mp4').disabled = false;
  document.getElementById('btn-export-gif').disabled = false;
}

document.getElementById('btn-export-mp4').addEventListener('click', () => doExport('mp4'));
document.getElementById('btn-export-gif').addEventListener('click', () => doExport('gif'));

function formatTime(sec) {
  const m = Math.floor(sec / 60), s = Math.floor(sec % 60);
  return `${m}:${s.toString().padStart(2,'0')}`;
}
function setStatus(msg) { document.getElementById('status').textContent = msg; }
```

- [ ] **Step 4：提交**

```bash
git add web/static/index.html web/static/app.js web/static/canvas-renderer.js
git commit -m "feat: 实现 Web UI — Canvas 实时渲染 + 四种风格 + 导出功能"
```

---

## Task 8：README 文档 + 端到端验证

**文件：**
- 创建：`musicvision/README.md`

- [ ] **Step 1：创建 `README.md`（中文）**

```markdown
# MusicVision

输入音乐文件，自动生成酷炫可视化视频。

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
brew install ffmpeg  # macOS（Linux: apt install ffmpeg）
```

### CLI 使用

```bash
python cli.py song.mp3                         # 自动选择风格，导出 MP4
python cli.py song.mp3 --style particle        # 指定粒子爆炸风格
python cli.py song.mp3 --format gif --fps 15   # 导出 GIF
```

### Web UI 使用

```bash
cd web && uvicorn server:app --reload
# 打开 http://localhost:8000
```

## 支持的风格

| 风格 | 参数 | 适合音乐类型 |
|------|------|------------|
| 频谱条形 | spectrum | 电子/说唱 |
| 波形流动 | waveform | 流行/民谣/古典 |
| 粒子爆炸 | particle | EDM/摇滚/嘻哈 |
| 环形放射 | circular | 全类型 |

## 新增自定义风格

在 `visualizers/` 目录下新建文件（如 `visualizers/mystyle.py`），继承 `BaseVisualizer`：

```python
from visualizers.base import BaseVisualizer
from core.analyzer import AudioFeatures
import numpy as np

class MyVisualizer(BaseVisualizer):
    name = "myname"
    display_name = "我的风格"

    def render_frame(self, features, frame_idx, width, height):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        # ... 绘制逻辑 ...
        return frame
```

重启服务后自动发现，无需修改其他文件。
```

- [ ] **Step 2：端到端 CLI 测试**

```bash
# 准备一段音频文件（任意 MP3/WAV）
python cli.py test_audio.mp3 --fps 5 --width 640 --height 360 --output test_out.mp4
# 预期：✅ 已导出 test_out.mp4
open test_out.mp4  # 验证视频可以播放
```

- [ ] **Step 3：端到端 Web 测试**

```bash
cd musicvision/web && uvicorn server:app --reload
# 浏览器打开 http://localhost:8000
# 拖入音频文件 → 等待分析 → 查看实时可视化 → 点击导出 MP4
```

- [ ] **Step 4：运行全部测试**

```bash
cd musicvision && python -m pytest tests/ -v
# 预期：全部通过
```

- [ ] **Step 5：最终提交**

```bash
git add README.md
git commit -m "docs: 添加 README 中文文档"
git push origin main
```

---

## 自检（规格覆盖验证）

| 需求 | 对应 Task |
|------|-----------|
| 输入 MP3/WAV/FLAC/OGG | Task 2 AudioAnalyzer |
| 自动分析 BPM/频谱/能量/调式 | Task 2 |
| 自动配色推导 | Task 2 _PALETTES |
| 频谱条形风格 | Task 3/5 |
| 波形流动风格 | Task 3/5 |
| 粒子爆炸风格 | Task 3/5 |
| 环形放射风格 | Task 3/5 |
| 插件式扩展（新增风格不改其他文件） | Task 3 VisualizerEngine |
| CLI 批处理 | Task 4 cli.py |
| Web 实时预览 | Task 6/7 |
| MP4 导出 | Task 4/6 |
| GIF 导出 | Task 4/6 |
| 左侧控制面板 + 右侧 Canvas | Task 7 index.html |
| 风格选择器 / 文件上传 / 音乐信息 / 导出按钮 | Task 7 app.js |
