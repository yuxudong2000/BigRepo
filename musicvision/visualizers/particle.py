import numpy as np
from visualizers.base import BaseVisualizer
from core.analyzer import AudioFeatures


class ParticleVisualizer(BaseVisualizer):
    name = "particle"
    display_name = "粒子爆炸"

    def render_frame(self, features: AudioFeatures, frame_idx: int,
                     width: int, height: int) -> np.ndarray:
        return np.zeros((height, width, 3), dtype=np.uint8)
