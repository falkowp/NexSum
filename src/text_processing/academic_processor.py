import re
from typing import Dict, List
from src.core.processor import BaseProcessor
from config.models import ProcessingResult
from src.text_processing.base_processor import TextPreprocessor
from src.models.extractors import AcademicElementsExtractor
from src.models.summarizer import TextSummarizer

class AcademicProcessor(BaseProcessor):
    """Process academic content (lectures, research papers, etc.)"""
    
    def __init__(self):
        self.extractor = AcademicElementsExtractor()
        self.summarizer = TextSummarizer()
    
    def can_process(self, content_type: str) -> bool:
        return content_type == 'academic'
    
    def process(self, text: str) -> ProcessingResult:
        # Preprocess academic text
        processed_text = self._preprocess_academic_text(text)
        
        # Extract academic elements
        elements = self.extractor.extract(processed_text)
        
        # Generate summary
        summary = self.summarizer.summarize(processed_text)
        
        return ProcessingResult(
            content_type='academic',
            summary=summary,
            metadata={
                "key_concepts": elements["key_concepts"],
                "learning_objectives": elements["learning_objectives"],
                "main_topics": elements["main_topics"],
                "key_definitions": elements["key_definitions"]
            },
            raw_text=text
        )
    
    def _preprocess_academic_text(self, text: str) -> str:
        text = TextPreprocessor.clean_text(text)
        # Ensure proper sentence structure for academic content
        text = re.sub(r'\.(\s*[a-z])', lambda m: '. ' + m.group(1).upper(), text)
        return text