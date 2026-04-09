#!/usr/bin/env python3
"""MusicVision CLI — 音乐可视化视频生成工具"""
import argparse
import os
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="MusicVision: 音乐 → 可视化视频")
    parser.add_argument("audio", help="音频文件路径（MP3/WAV/FLAC/OGG）")
    parser.add_argument("--style", default="auto",
                        choices=["auto", "spectrum", "waveform", "particle", "circular"],
                        help="可视化风格（默认 auto：自动选择）")
    parser.add_argument("--output", default=None, help="输出文件路径（默认：<input>_viz.mp4）")
    parser.add_argument("--format", default="mp4", choices=["mp4", "gif"])
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    args = parser.parse_args()

    # 延迟导入，避免慢速导入影响 --help 响应
    from core.analyzer import AudioAnalyzer
    from core.engine import VisualizerEngine
    from core.renderer_cli import CLIRenderer

    if not os.path.exists(args.audio):
        print(f"错误：找不到文件 {args.audio}", file=sys.stderr)
        sys.exit(1)

    output = args.output or str(Path(args.audio).stem + f"_viz.{args.format}")

    print(f"🎵 正在分析音频: {args.audio}")
    analyzer = AudioAnalyzer()
    features = analyzer.analyze(args.audio)
    print(f"   BPM: {features.bpm:.1f} | 调: {features.key} | 时长: {features.duration:.1f}s")

    style = args.style
    if style == "auto":
        avg = float(features.energy.mean())
        style = "particle" if avg > 0.1 else ("waveform" if avg < 0.03 else "spectrum")
        print(f"   自动选择风格: {style}")

    engine = VisualizerEngine()
    renderer = CLIRenderer(engine)
    print(f"🎨 开始渲染 ({args.width}x{args.height} @ {args.fps}fps)...")
    renderer.render(features, args.audio, output,
                    style=style, fps=args.fps, width=args.width, height=args.height)
    print(f"✅ 已导出: {output}")


if __name__ == "__main__":
    main()
