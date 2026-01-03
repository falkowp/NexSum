"""Simple benchmark for transcriber backends.
Usage:
  python scripts/benchmark_transcriber.py /path/to/audio/file.wav

It will run the current configured backend (TRANSCRIBER_BACKEND env var) and measure wall time.
"""
import time
import sys
import os
from pathlib import Path

from src.transcription.transcriber import transcribe_audio_bytes


def main(audio_path: str):
    p = Path(audio_path)
    if not p.exists():
        print('File not found:', audio_path)
        return 2

    audio_bytes = p.read_bytes()
    for i in range(3):
        start = time.time()
        text = transcribe_audio_bytes(audio_bytes)
        dt = time.time() - start
        print(f'Run {i+1}: {dt:.2f}s; {len(text)} chars')

    return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python scripts/benchmark_transcriber.py /path/to/audio')
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
