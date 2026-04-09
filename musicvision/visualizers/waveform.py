import numpy as np
from visualizers.base import BaseVisualizer
from core.analyzer import AudioFeatures


class WaveformVisualizer(BaseVisualizer):
    name = "waveform"
    display_name = "波形流动"

    def render_frame(self, features: AudioFeatures, frame_idx: int,
                     width: int, height: int) -> np.ndarray:
        return np.zeros((height, width, 3), dtype=np.uint8)
