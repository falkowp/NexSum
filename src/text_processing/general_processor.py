from typing import Dict, List
from ..core.processor import BaseProcessor
from ..config.models import ProcessingResult
from ..text_processing.base_processor import TextPreprocessor
from ..models.extractors import GeneralElementsExtractor
#from src.models.summarizer import TextSummarizer
from ..models import TextSummarizer

class GeneralProcessor(BaseProcessor):
    """Process general content (fallback for unspecified types)"""
    
    def __init__(self):
        self.extractor = GeneralElementsExtractor()
        self.summarizer = TextSummarizer()
    
    def can_process(self, content_type: str) -> bool:
        return content_type == 'general'
    
    def process(self, text: str) -> ProcessingResult:
        # Preprocess general text
        processed_text = TextPreprocessor.clean_text(text)
        
        # Extract general elements
        elements = self.extractor.extract(processed_text)
        
        # Generate summary
        summary = self.summarizer.summarize(processed_text)
        
        return ProcessingResult(
            content_type='general',
            summary=summary,
            metadata={
                "key_points": elements["key_points"],
                "main_ideas": elements["main_ideas"],
                "actionable_items": elements["actionable_items"]
            },
            raw_text=text
        )