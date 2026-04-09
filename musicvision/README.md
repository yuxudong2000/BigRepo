# MusicVision

输入音乐文件，全自动生成酷炫可视化视频。

## 功能

- 自动分析 BPM、节拍、频谱、能量、音调
- 四种内置可视化风格：频谱条形、波形流动、粒子爆炸、环形放射
- 自动推导颜色方案（根据音乐能量和调式）
- 浏览器实时预览 + 导出 MP4/GIF
- CLI 批量处理模式

## 快速开始

### 1. 安装依赖

```bash
cd musicvision
pip install -r requirements.txt
brew install ffmpeg   # macOS
# Ubuntu: apt install ffmpeg
```

### 2. CLI 使用

```bash
# 自动选择风格，导出 MP4
python cli.py song.mp3

# 指定风格
python cli.py song.mp3 --style particle

# 导出 GIF（低帧率）
python cli.py song.mp3 --format gif --fps 15

# 自定义分辨率
python cli.py song.mp3 --width 1280 --height 720 --output my_video.mp4
```

### 3. Web UI 使用

```bash
cd musicvision/web
uvicorn server:app --reload
# 打开浏览器访问 http://localhost:8000
```

拖拽音频文件到页面 → 等待分析 → 实时预览 → 点击导出。

## 可视化风格

| 风格 | 参数值 | 特点 | 适合音乐 |
|------|--------|------|---------|
| 频谱条形 | `spectrum` | 霓虹垂直柱随频谱跳动 | 电子/说唱 |
| 波形流动 | `waveform` | 渐变色平滑波形线 | 流行/民谣/古典 |
| 粒子爆炸 | `particle` | 节拍时粒子向外爆炸扩散 | EDM/摇滚/嘻哈 |
| 环形放射 | `circular` | 圆心放射状频谱，随 BPM 旋转 | 全类型 |

## 新增自定义风格

在 `visualizers/` 目录下新建文件，继承 `BaseVisualizer`：

```python
# visualizers/mystyle.py
from visualizers.base import BaseVisualizer
from core.analyzer import AudioFeatures
import numpy as np

class MyVisualizer(BaseVisualizer):
    name = "mystyle"           # 唯一标识符
    display_name = "我的风格"   # 展示名称

    def render_frame(self, features: AudioFeatures, frame_idx: int,
                     width: int, height: int) -> np.ndarray:
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        # 在这里实现你的绘制逻辑
        # features.spectrum[:, frame_idx] — 当前帧频谱
        # features.energy[frame_idx]      — 当前帧能量
        # features.beat_times             — 节拍时间点列表
        # features.palette                — 自动推断的配色
        return frame
```

重启服务后自动发现，无需修改其他文件。Web UI 和 CLI 均可立即使用新风格。

## 运行测试

```bash
cd musicvision
python -m pytest tests/ -v
```

## 项目结构

```
musicvision/
├── core/
│   ├── analyzer.py       # 音频分析：BPM/频谱/能量/配色
│   ├── engine.py         # 可视化引擎 + 插件自动发现
│   └── renderer_cli.py   # CLI 逐帧渲染 → moviepy 合成
├── visualizers/
│   ├── base.py           # BaseVisualizer 抽象基类
│   ├── spectrum.py       # 频谱条形
│   ├── waveform.py       # 波形流动
│   ├── particle.py       # 粒子爆炸
│   └── circular.py       # 环形放射
├── web/
│   ├── server.py         # FastAPI Web 服务
│   └── static/           # 前端 HTML/JS
├── tests/                # 单元测试
├── cli.py                # CLI 入口
└── requirements.txt
```
