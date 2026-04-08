# MusicVision 设计规格文档

**日期：** 2026-04-08  
**状态：** 已确认

---

## 概述

MusicVision 是一款音乐可视化工具。输入音频文件后，系统自动分析其音乐属性（BPM、节拍时间点、频谱、能量），并生成视觉效果酷炫的动画视频。支持四种内置可视化风格，采用插件架构便于后续扩展。

**输出目标：** 浏览器实时预览 + MP4/GIF 导出

---

## 需求

### 输入
- 音频文件格式：MP3、WAV、FLAC、OGG
- 可视化风格选择（默认根据音乐分析结果自动选择）

### 输出
- 浏览器实时预览（Canvas 渲染）
- MP4 视频导出
- GIF 动图导出

### 使用方式
- **Web UI**：拖拽音频文件到浏览器，实时预览，点击导出
- **CLI**：`python cli.py song.mp3 [--style spectrum] [--output out.mp4]`，用于批量处理

### 自动化程度
所有可视化参数（颜色、速度、强度、粒子数量等）均由音频分析结果自动推导，无需手动调整。

---

## 系统架构

```
音频文件
    │
    ▼
AudioAnalyzer（librosa 音频分析）
    │  BPM、节拍时间点、频谱、能量、自动配色
    ▼
VisualizerEngine（可视化引擎 + 插件注册表）
    │
    ▼
 ┌─────────────────────────────┐
 │  Visualizer 插件接口         │
 │  （每种风格一个独立文件）     │
 └─────────────────────────────┘
         │                │
         ▼                ▼
  Web 渲染器          CLI 渲染器
  （Canvas/SSE）      （逐帧渲染）
         │                │
         ▼                ▼
   浏览器实时预览     moviepy → MP4/GIF
```

---

## 核心模块说明

### `core/analyzer.py` — 音频分析器

职责：
- 使用 `librosa.load()` 加载音频
- 提取 BPM 和节拍帧索引（`librosa.beat.beat_track`）
- 计算短时傅里叶变换（`librosa.stft`），得到每帧频谱幅值
- 计算每帧 RMS 能量（`librosa.feature.rms`）
- 推断 `auto_palette`：根据能量级别和音乐调式（大/小调）自动选择配色方案
- 检测音调（Key），例如 "Am"

输出数据结构 `AudioFeatures`（Python dataclass）：

```python
@dataclass
class AudioFeatures:
    bpm: float
    beat_times: list[float]     # 节拍时间点（秒）
    duration: float             # 总时长（秒）
    sample_rate: int
    hop_length: int             # 帧步长
    spectrum: np.ndarray        # 形状 (n_fft_bins, n_frames)，每帧频谱
    energy: np.ndarray          # 形状 (n_frames,)，每帧能量
    palette: ColorPalette       # 自动推断的配色
    key: str                    # 音调，例如 "Am"
```

---

### `core/engine.py` — 可视化引擎

职责：
- 维护插件注册表（name → 插件类的映射字典）
- 启动时自动扫描 `visualizers/` 目录，发现并注册所有继承 `BaseVisualizer` 的类
- 对外暴露 `render_frame(features, frame_idx) -> np.ndarray`
- 对外暴露 `list_plugins() -> list[str]`

插件自动发现机制：扫描 `visualizers/*.py`，导入所有继承 `BaseVisualizer` 的类，无需手动注册。

---

### `visualizers/base.py` — 基类（抽象）

```python
class BaseVisualizer(ABC):
    name: str          # 唯一标识符，例如 "spectrum"
    display_name: str  # 展示名称，例如 "频谱条形"

    @abstractmethod
    def render_frame(self, features: AudioFeatures, frame_idx: int,
                     width: int, height: int) -> np.ndarray:
        """返回 BGR 格式的 numpy 图像数组"""
```

---

### 四种内置可视化风格

| 文件 | 风格名称 | 核心视觉元素 |
|------|----------|-------------|
| `visualizers/spectrum.py` | 频谱条形 Spectrum Bars | 霓虹垂直柱，高度 = FFT 幅值，颜色随配色变化 |
| `visualizers/waveform.py` | 波形流动 Waveform Flow | 渐变色平滑波形线，随振幅起伏 |
| `visualizers/particle.py` | 粒子爆炸 Particle Burst | 粒子在节拍时向外爆炸扩散，强拍时发光 |
| `visualizers/circular.py` | 环形放射 Circular Radial | 圆心放射状频谱柱，随 BPM 旋转 |

**扩展方式：** 新建 `visualizers/newstyle.py` 继承 `BaseVisualizer`，系统启动时自动发现，无需修改其他文件。

---

### `core/renderer_cli.py` — CLI 渲染器

- 以 30fps 遍历所有帧
- 每帧调用 `visualizer.render_frame()` 获取 numpy 图像数组
- 使用 `moviepy.ImageSequenceClip` 合成帧序列
- 通过 `moviepy.AudioFileClip` 混入原始音频
- 导出 MP4（H.264）或 GIF

---

### `web/server.py` — FastAPI 服务

API 端点：

```
POST /analyze              body: {file}            → 返回 AudioFeatures JSON + job_id
GET  /stream/{job_id}      SSE 流                  → 推送每帧特征数据（频谱切片 + 能量值）
POST /export/{job_id}      body: {format, style}   → 后台启动导出任务
GET  /export/{job_id}/download                     → 返回导出文件
GET  /plugins                                      → 返回可用插件列表
```

---

### `web/static/` — 前端

- 单页应用：`index.html` + `app.js` + `canvas-renderer.js`
- 布局：**左侧控制面板（固定宽度）** | **右侧 Canvas 画布（自适应）**
  - 左侧：风格选择器、文件上传/拖拽区、音乐信息（BPM/Key/能量条）、导出按钮
  - 右侧：`<canvas>` 实时可视化区域，底部为播放控制条
- `canvas-renderer.js` 通过 SSE 接收每帧特征数据，在 Canvas 上调用对应风格的 JS 绘制函数
- 导出流程：触发 `/export` 接口 → 轮询进度 → 完成后触发文件下载

---

### `cli.py` — 命令行入口

```bash
python cli.py <音频文件> [选项]

选项：
  --style    spectrum|waveform|particle|circular  （默认：auto，自动选择）
  --output   输出文件路径（默认：<输入文件名>_viz.mp4）
  --format   mp4|gif（默认：mp4）
  --fps      帧率（默认：30）
  --width    视频宽度（默认：1920）
  --height   视频高度（默认：1080）
```

---

## 项目目录结构

```
musicvision/
├── core/
│   ├── __init__.py
│   ├── analyzer.py          # 音频分析器 + AudioFeatures 数据类
│   ├── engine.py            # 可视化引擎 + 插件注册表
│   └── renderer_cli.py      # CLI 逐帧渲染器
├── visualizers/
│   ├── base.py              # BaseVisualizer 抽象基类
│   ├── spectrum.py          # 频谱条形
│   ├── waveform.py          # 波形流动
│   ├── particle.py          # 粒子爆炸
│   └── circular.py          # 环形放射
├── web/
│   ├── server.py            # FastAPI 应用
│   └── static/
│       ├── index.html
│       ├── app.js
│       └── canvas-renderer.js
├── cli.py                   # 命令行入口
├── requirements.txt
└── README.md
```

---

## 依赖项

Python 包：

```
librosa>=0.10
numpy
moviepy>=1.0
fastapi
uvicorn
python-multipart
pillow
```

系统依赖：`ffmpeg`（需单独安装）

---

## 自动配色逻辑

| 音乐属性 | 配色方案 |
|----------|----------|
| 高能量 + 大调 | 暖色系：橙/黄/红 |
| 高能量 + 小调 | 电光色：青/紫/品红 |
| 低能量 + 大调 | 柔和色：浅青/绿 |
| 低能量 + 小调 | 深邃色：靛蓝/紫罗兰 |

---

## Web 模式数据流

1. 用户拖入文件 → `POST /analyze` → 服务端运行 `AudioAnalyzer` → 返回 `AudioFeatures` JSON + job_id
2. 前端收到特征数据，建立 SSE 连接至 `/stream/{job_id}`
3. 服务端推送预计算的逐帧数据（频谱切片 + 能量值）
4. `canvas-renderer.js` 收到帧消息，调用当前风格的 JS 绘制函数渲染到 Canvas
5. 用户点击导出 → `POST /export/{job_id}` → 服务端后台运行 CLI 渲染器 → SSE 进度推送 → 完成后返回下载链接

---

## 扩展点

- **新增可视化风格**：在 `visualizers/` 下新建 `.py` 文件，继承 `BaseVisualizer`，系统启动时自动发现
- **新增导出格式**：扩展 `renderer_cli.py` 的格式处理逻辑
- **新增音频特征**：在 `AudioFeatures` 中新增字段，更新 `analyzer.py`
