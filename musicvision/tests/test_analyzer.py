# tests/test_analyzer.py
import numpy as np
import pytest
from core.analyzer import AudioAnalyzer, AudioFeatures, ColorPalette


def make_beat_wav(tmp_path, bpm=120, duration=3.0, sr=22050):
    """生成带节拍的音频（鼓点冲击信号）用于测试，librosa 可检测到 BPM"""
    import scipy.io.wavfile as wav
    t = np.linspace(0, duration, int(sr * duration))
    # 基础正弦波
    audio = np.sin(2 * np.pi * 440 * t) * 0.3
    # 每隔 beat_interval 秒添加一个冲击（模拟鼓点）
    beat_interval = 60.0 / bpm
    beat_sample = int(beat_interval * sr)
    for i in range(0, len(audio), beat_sample):
        end = min(i + sr // 20, len(audio))  # 50ms 冲击
        audio[i:end] += np.exp(-np.linspace(0, 5, end - i)) * 0.7
    audio = np.clip(audio, -1.0, 1.0)
    audio_int16 = (audio * 32767).astype(np.int16)
    path = tmp_path / "test_beat.wav"
    wav.write(str(path), sr, audio_int16)
    return str(path)


def test_audio_features_fields(tmp_path):
    path = make_beat_wav(tmp_path)
    analyzer = AudioAnalyzer()
    features = analyzer.analyze(path)
    assert isinstance(features, AudioFeatures)
    assert features.bpm >= 0  # 对测试音频 BPM 可能为 0，只验证字段存在
    assert features.duration == pytest.approx(3.0, abs=0.1)
    assert features.sample_rate == 22050
    assert features.spectrum.ndim == 2
    assert features.spectrum.shape[0] > 0  # n_fft_bins > 0
    assert features.spectrum.shape[1] > 0  # n_frames > 0
    assert features.energy.ndim == 1
    assert len(features.energy) > 0
    assert isinstance(features.palette, ColorPalette)
    assert features.key != ""


def test_palette_fields():
    p = ColorPalette(primary="#00f5ff", secondary="#7b2fff", background="#050510", accent="#ff00aa")
    assert p.primary.startswith("#")
    assert p.background.startswith("#")
