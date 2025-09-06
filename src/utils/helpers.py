import re
from pathlib import Path

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x20-\x7E]', '', text)
    return text.strip()