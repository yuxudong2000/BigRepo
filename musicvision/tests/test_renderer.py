# tests/test_renderer.py
import numpy as np
import pytest
from core.analyzer import AudioFeatures, ColorPalette
from core.engine import VisualizerEngine
from core.renderer_cli import CLIRenderer


def _dummy_features() -> AudioFeatures:
    sr = 22050
    hop = 512
    n_frames = 50
    return AudioFeatures(
        bpm=120.0, beat_times=[0.5, 1.0],
        duration=1.0, sample_rate=sr, hop_length=hop,
        spectrum=np.random.rand(513, n_frames),
        energy=np.random.rand(n_frames),
        palette=ColorPalette("#00f5ff", "#7b2fff", "#050510", "#ff00aa"),
        key="Am",
    )


def test_renderer_creates_mp4(tmp_path):
    import scipy.io.wavfile as wav
    # 生成 1 秒音频
    sr = 22050
    audio = (np.sin(2 * np.pi * 440 * np.linspace(0, 1, sr)) * 32767).astype(np.int16)
    audio_path = str(tmp_path / "input.wav")
    wav.write(audio_path, sr, audio)

    output_path = str(tmp_path / "output.mp4")
    features = _dummy_features()
    engine = VisualizerEngine()
    renderer = CLIRenderer(engine)
    renderer.render(features, audio_path, output_path, style="spectrum",
                    fps=10, width=320, height=180)

    assert (tmp_path / "output.mp4").exists()
    assert (tmp_path / "output.mp4").stat().st_size > 0
