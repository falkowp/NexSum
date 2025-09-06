import re
import nltk
from typing import List, Dict, Any
from src.core.processor import BaseProcessor
from config.models import ProcessingResult
from src.utils.helpers import clean_text

class TextPreprocessor:
    """Handle text preprocessing operations"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        return clean_text(text)
    
    @staticmethod
    def remove_filler_words(text: str, filler_words: List[str]) -> str:
        for word in filler_words:
            text = re.sub(rf'\b{word}\b', '', text, flags=re.IGNORECASE)
        return text
    
    @staticmethod
    def structure_speaker_turns(text: str) -> str:
        return re.sub(r'([A-Z][a-z]+):', r'\n\1: ', text)