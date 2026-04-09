from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import librosa


@dataclass
class ColorPalette:
    primary: str
    secondary: str
    background: str
    accent: str


@dataclass
class AudioFeatures:
    bpm: float
    beat_times: list[float]
    duration: float
    sample_rate: int
    hop_length: int
    spectrum: np.ndarray      # shape: (n_fft_bins, n_frames)
    energy: np.ndarray        # shape: (n_frames,)
    palette: ColorPalette
    key: str


# 四种预设配色，根据 (高/低能量) × (大/小调) 选择
_PALETTES = {
    ("high", "major"): ColorPalette("#ffaa00", "#ff4400", "#0a0500", "#ffdd00"),
    ("high", "minor"): ColorPalette("#00f5ff", "#7b2fff", "#050510", "#ff00aa"),
    ("low",  "major"): ColorPalette("#00e5aa", "#00b5d8", "#020d0a", "#88ffcc"),
    ("low",  "minor"): ColorPalette("#6644cc", "#220066", "#030008", "#aa66ff"),
}

# 色度轮 —— 检测音调所用
_CHROMA_NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


class AudioAnalyzer:
    def analyze(self, filepath: str, hop_length: int = 512) -> AudioFeatures:
        y, sr = librosa.load(filepath, sr=None, mono=True)
        duration = librosa.get_duration(y=y, sr=sr)

        # BPM & 节拍
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop_length)
        bpm = float(tempo) if np.isscalar(tempo) else float(tempo[0])
        beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=hop_length).tolist()

        # 频谱
        stft = np.abs(librosa.stft(y, hop_length=hop_length))  # (n_fft_bins, n_frames)

        # 能量
        rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]  # (n_frames,)

        # 调式检测
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        key_idx = int(np.argmax(chroma.mean(axis=1)))
        key_note = _CHROMA_NOTES[key_idx]
        # 简单大/小调判断：比较大三度和小三度的色度能量
        major_energy = chroma[(key_idx + 4) % 12].mean()
        minor_energy = chroma[(key_idx + 3) % 12].mean()
        mode = "major" if major_energy >= minor_energy else "minor"
        key = f"{key_note}{'m' if mode == 'minor' else ''}"

        # 配色选择
        avg_energy = float(rms.mean())
        energy_level = "high" if avg_energy > 0.05 else "low"
        palette = _PALETTES[(energy_level, mode)]

        return AudioFeatures(
            bpm=bpm,
            beat_times=beat_times,
            duration=duration,
            sample_rate=sr,
            hop_length=hop_length,
            spectrum=stft,
            energy=rms,
            palette=palette,
            key=key,
        )
