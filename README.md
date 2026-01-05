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

## Embeddings-based content classifier (recommended)

To get better, context-aware content-type detection, train the embeddings-based classifier:

- Install additional dependencies: `pip install sentence-transformers` (requires `torch`).
- Train with:

```
python scripts/train_content_classifier_embeddings.py --data-dir test_data --embed-model all-MiniLM-L6-v2
```

- The trained model is saved to `src/models/content_classifier_embeddings.joblib` and will be used by the `ContentTypeDetector` when available.
