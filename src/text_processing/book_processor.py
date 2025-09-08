import re
from typing import Dict, List
from core.processor import BaseProcessor
from config.models import ProcessingResult
from text_processing.base_processor import TextPreprocessor
from models.extractors import BookElementsExtractor
#from src.models.summarizer import TextSummarizer
from models import TextSummarizer

class BookProcessor(BaseProcessor):
    """Process book content (fiction, non-fiction, etc.)"""
    
    def __init__(self):
        self.extractor = BookElementsExtractor()
        self.summarizer = TextSummarizer()
    
    def can_process(self, content_type: str) -> bool:
        return content_type == 'book'
    
    def process(self, text: str) -> ProcessingResult:
        # Preprocess book text
        processed_text = self._preprocess_book_text(text)
        
        # Extract book elements
        elements = self.extractor.extract(processed_text)
        
        # Generate summary
        summary = self.summarizer.summarize(processed_text)
        
        return ProcessingResult(
            content_type='book',
            summary=summary,
            metadata={
                "key_characters": elements["key_characters"],
                "major_themes": elements["major_themes"],
                "plot_points": elements["plot_points"],
                "setting": elements["setting"]
            },
            raw_text=text
        )
    
    def _preprocess_book_text(self, text: str) -> str:
        text = TextPreprocessor.clean_text(text)
        # Handle paragraph breaks for book content
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text