from typing import Tuple

from src.transcription.transcriber import process_audio_pipeline

def transcribe_audio_bytes(audio_bytes: bytes) -> Tuple[str, str]:
    return process_audio_pipeline(audio_bytes)
