import re
import logging
from pathlib import Path

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def validate_text(text):
    if not text or not isinstance(text, str):
        raise ValueError("Input must be a non-empty string")
    
    if len(text.strip()) < 50:
        raise ValueError("Text is too short for processing")
    
    return text.strip()

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x20-\x7E]', '', text)
    return text.strip()