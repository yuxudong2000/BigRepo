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

        segment = max(1, width // 64)
        for i in range(0, width - segment, segment):
            t = i / width
            color = tuple(int(color_a[c] * (1 - t) + color_b[c] * t) for c in range(3))
            thickness = 2 + int(energy * 3)
            cv2.line(frame, points[i], points[i + segment], color, thickness, cv2.LINE_AA)

        # 镜像下半部分（对称波形，半透明）
        for x in range(width):
            y_top = points[x][1]
            y_bot = height - (center_y - y_top) - 1
            if 0 <= y_bot < height:
                t = x / width
                color = tuple(int(color_a[c] * (1 - t) + color_b[c] * t) for c in range(3))
                frame[y_bot, x] = [c // 2 for c in color]

        return frame
