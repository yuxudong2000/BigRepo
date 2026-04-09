from __future__ import annotations
import importlib
import pkgutil
import visualizers
from visualizers.base import BaseVisualizer
from core.analyzer import AudioFeatures
import numpy as np


class VisualizerEngine:
    def __init__(self):
        self._registry: dict[str, BaseVisualizer] = {}
        self._auto_discover()

    def _auto_discover(self):
        """扫描 visualizers/ 包，自动注册所有 BaseVisualizer 子类"""
        for finder, module_name, _ in pkgutil.iter_modules(visualizers.__path__):
            if module_name == "base":
                continue
            module = importlib.import_module(f"visualizers.{module_name}")
            for attr_name in dir(module):
                obj = getattr(module, attr_name)
                if (isinstance(obj, type)
                        and issubclass(obj, BaseVisualizer)
                        and obj is not BaseVisualizer
                        and hasattr(obj, "name")):
                    instance = obj()
                    self._registry[instance.name] = instance

    def list_plugins(self) -> list[str]:
        return list(self._registry.keys())

    def render_frame(self, style: str, features: AudioFeatures,
                     frame_idx: int, width: int = 1920, height: int = 1080) -> np.ndarray:
        if style not in self._registry:
            raise ValueError(f"未知风格: {style}，可用: {self.list_plugins()}")
        return self._registry[style].render_frame(features, frame_idx, width, height)
