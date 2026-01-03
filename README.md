# NexSum - Abstractive Text Summarization Model

A from-scratch implementation of a Seq2Seq model with attention for abstractive text summarization.

## Project Structure

## GPU-accelerated transcription (optional)

If you have an NVIDIA GPU and want faster transcription, install `faster-whisper` and set the backend:

- Install:
  - pip install "faster-whisper>=0.5.0"
- Set environment variables (example, PowerShell):
  - $env:TRANSCRIBER_BACKEND = "faster-whisper"
  - $env:WHISPER_MODEL = "small"  # choose tiny / small / base / large depending on speed/accuracy

You can run the included benchmark to measure performance:

```
python scripts/benchmark_transcriber.py path/to/sample.wav
```

If `faster-whisper` is not installed, the system falls back to the existing `whisper` backend (which will use CUDA if available).

