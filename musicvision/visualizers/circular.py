import numpy as np
from visualizers.base import BaseVisualizer
from core.analyzer import AudioFeatures


class CircularVisualizer(BaseVisualizer):
    name = "circular"
    display_name = "环形放射"

    def render_frame(self, features: AudioFeatures, frame_idx: int,
                     width: int, height: int) -> np.ndarray:
        return np.zeros((height, width, 3), dtype=np.uint8)
