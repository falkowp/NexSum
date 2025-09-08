# Thin wrapper around your existing pipeline so routes stay clean
from typing import Tuple

# Import your transcriber from src/
from src.transcription.transcriber import process_audio_pipeline

def transcribe_audio_bytes(audio_bytes: bytes) -> Tuple[str, str]:
    """
    Returns (raw_text, polished_text)
    """
    return process_audio_pipeline(audio_bytes)
