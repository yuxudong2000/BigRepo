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

        # 取当前帧频谱（前 128 个 bin）
        spec = features.spectrum[:128, frame_idx]
        spec = spec / (spec.max() + 1e-8)

        n_bars = 64
        bar_w = max(1, width // n_bars)
        energy = float(features.energy[frame_idx]) / (features.energy.max() + 1e-8)

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

            t = i / n_bars
            color = tuple(int(color_start[c] * (1 - t) + color_end[c] * t) for c in range(3))
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)

            # 顶部发光点
            glow_color = tuple(min(255, int(c * 1.5)) for c in color)
            cv2.rectangle(frame, (x1, y1), (x2, y1 + 3), glow_color, -1)

        return frame
