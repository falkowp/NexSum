import re
import nltk
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..config.models import ProcessingResult
from ..utils.helpers import clean_text


class BaseProcessor(ABC):
    """Abstract base class for all content processors"""
    
    @abstractmethod
    def process(self, text: str) -> ProcessingResult:
        pass
    
    @abstractmethod
    def can_process(self, content_type: str) -> bool:
        pass


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