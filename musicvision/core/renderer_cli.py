from __future__ import annotations
import numpy as np
from moviepy import ImageSequenceClip, AudioFileClip
from core.analyzer import AudioFeatures
from core.engine import VisualizerEngine


class CLIRenderer:
    def __init__(self, engine: VisualizerEngine):
        self.engine = engine

    def render(self, features: AudioFeatures, audio_path: str,
               output_path: str, style: str = "spectrum",
               fps: int = 30, width: int = 1920, height: int = 1080) -> None:
        """逐帧渲染并导出 MP4 或 GIF"""
        total_frames = int(features.duration * fps)
        feature_frames = features.spectrum.shape[1]

        frames: list[np.ndarray] = []
        for i in range(total_frames):
            # 将视频帧映射到 spectrum 帧索引
            feature_idx = int(i / total_frames * feature_frames)
            feature_idx = min(feature_idx, feature_frames - 1)
            bgr = self.engine.render_frame(style, features, feature_idx, width, height)
            # moviepy 需要 RGB
            rgb = bgr[:, :, ::-1]
            frames.append(rgb)

        clip = ImageSequenceClip(frames, fps=fps)
        audio = AudioFileClip(audio_path).subclipped(0, features.duration)
        clip = clip.with_audio(audio)

        if output_path.endswith(".gif"):
            clip.write_gif(output_path, fps=fps)
        else:
            clip.write_videofile(output_path, fps=fps, codec="libx264",
                                 audio_codec="aac", logger=None)
