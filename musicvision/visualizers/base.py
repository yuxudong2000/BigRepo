from abc import ABC, abstractmethod
import numpy as np
from core.analyzer import AudioFeatures


class BaseVisualizer(ABC):
    name: str          # 唯一标识符，如 "spectrum"
    display_name: str  # 展示名称，如 "频谱条形"

    @abstractmethod
    def render_frame(self, features: AudioFeatures, frame_idx: int,
                     width: int, height: int) -> np.ndarray:
        """渲染单帧，返回 shape=(height, width, 3) 的 uint8 BGR 图像"""
