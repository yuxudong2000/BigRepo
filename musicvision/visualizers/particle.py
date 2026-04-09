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
        rng = np.random.default_rng(frame_idx)

        energy = float(features.energy[frame_idx]) / (features.energy.max() + 1e-8)
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
            max_r = (0.6 if is_beat else 0.35) * min(width, height)
            radius = rng.uniform(0, max_r) * (0.3 + 0.7 * energy)
            px = int(cx + radius * np.cos(angle))
            py = int(cy + radius * np.sin(angle))

            if not (0 <= px < width and 0 <= py < height):
                continue

            color = colors[rng.integers(len(colors))]
            size = int(rng.integers(1, 5 if is_beat else 3))
            brightness = 0.4 + 0.6 * energy
            draw_color = tuple(int(c * brightness) for c in color)
            cv2.circle(frame, (px, py), max(1, size), draw_color, -1)

        # 中心发光核心
        glow_r = int(20 + energy * 40 + (30 if is_beat else 0))
        core_color = _hex_to_bgr(palette.primary)
        cv2.circle(frame, (cx, cy), glow_r, core_color, -1)
        cv2.circle(frame, (cx, cy), max(1, glow_r // 2), (255, 255, 255), -1)

        return frame
