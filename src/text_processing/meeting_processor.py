import re
import nltk
from typing import Dict, List, Any
from src.core.processor import BaseProcessor
from config.models import ProcessingResult
from src.text_processing.base_processor import TextPreprocessor
from src.models.extractors import MeetingElementsExtractor
from src.models.reliable_summarizer import TextSummarizer

class MeetingProcessor(BaseProcessor):
    """Process meeting transcripts"""
    
    def __init__(self):
        self.extractor = MeetingElementsExtractor()
        self.summarizer = TextSummarizer()
    
    def can_process(self, content_type: str) -> bool:
        return content_type == 'meeting'
    
    def process(self, text: str) -> ProcessingResult:
        # Preprocess meeting text
        processed_text = self._preprocess_meeting_text(text)
        
        # Extract meeting elements
        elements = self.extractor.extract(processed_text)
        
        # Generate summary
        summary = self.summarizer.summarize(processed_text)
        
        return ProcessingResult(
            content_type='meeting',
            summary=summary,
            metadata={
                "participants": elements["speakers"],
                "action_items": elements["action_items"],
                "decisions": elements["decisions"],
                "key_discussion_points": elements["key_points"]
            },
            raw_text=text
        )
    
    def _preprocess_meeting_text(self, text: str) -> str:
        text = TextPreprocessor.clean_text(text)
        text = TextPreprocessor.remove_filler_words(text, ['um', 'uh', 'like', 'you know'])
        text = TextPreprocessor.structure_speaker_turns(text)
        return text