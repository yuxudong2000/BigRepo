# tests/test_engine.py
import numpy as np
from core.engine import VisualizerEngine
from visualizers.base import BaseVisualizer
from core.analyzer import AudioFeatures, ColorPalette


def _dummy_features() -> AudioFeatures:
    sr = 22050
    hop = 512
    n_frames = 100
    return AudioFeatures(
        bpm=120.0, beat_times=[0.5, 1.0, 1.5],
        duration=3.0, sample_rate=sr, hop_length=hop,
        spectrum=np.random.rand(513, n_frames),
        energy=np.random.rand(n_frames),
        palette=ColorPalette("#00f5ff", "#7b2fff", "#050510", "#ff00aa"),
        key="Am",
    )


def test_engine_lists_builtin_plugins():
    engine = VisualizerEngine()
    plugins = engine.list_plugins()
    assert "spectrum" in plugins
    assert "waveform" in plugins
    assert "particle" in plugins
    assert "circular" in plugins


def test_engine_render_frame_returns_image():
    engine = VisualizerEngine()
    features = _dummy_features()
    frame = engine.render_frame("spectrum", features, frame_idx=0, width=320, height=180)
    assert frame.shape == (180, 320, 3)
    assert frame.dtype == np.uint8


def test_engine_unknown_style_raises():
    engine = VisualizerEngine()
    features = _dummy_features()
    try:
        engine.render_frame("nonexistent", features, frame_idx=0, width=320, height=180)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
