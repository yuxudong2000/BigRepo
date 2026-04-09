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
        base_r = int(min(width, height) * 0.15)
        max_bar = int(min(width, height) * 0.35)

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
        cv2.circle(frame, (cx, cy), max(1, int(base_r * 0.4)), inner_color, -1)

        return frame
