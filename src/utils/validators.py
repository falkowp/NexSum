from typing import Any
from ..config.settings import PROCESSING_SETTINGS

def validate_text(text: Any) -> str:
    """Validate input text"""
    if not text or not isinstance(text, str):
        raise ValueError("Input must be a non-empty string")
    
    text = text.strip()
    if len(text) < PROCESSING_SETTINGS["min_text_length"]:
        raise ValueError(f"Text is too short for processing (min {PROCESSING_SETTINGS['min_text_length']} chars)")
    
    return text