from .base_extractor import BaseExtractor
import re
import nltk
from typing import Dict, List, Any, Set
from collections import defaultdict
from abc import ABC, abstractmethod

class GeneralElementsExtractor(BaseExtractor):
    """Extract general content elements"""
    
    def extract(self, text: str) -> Dict[str, Any]:
        key_points = self._extract_main_topics(text)
        main_ideas = self._extract_main_ideas(text)
        actionable_items = self._extract_actionable_items(text)
        
        return {
            "key_points": key_points,
            "main_ideas": main_ideas,
            "actionable_items": actionable_items
        }
    
    def _extract_main_ideas(self, text: str) -> List[str]:
        """Extract main ideas from general text"""
        sentences = nltk.sent_tokenize(text)
        ideas = []
        
        idea_indicators = ['important', 'crucial', 'essential', 'key', 'main', 'primary']
        
        for sentence in sentences:
            if any(indicator in sentence.lower() for indicator in idea_indicators):
                ideas.append(sentence)
        
        return ideas[:3]
    
    def _extract_actionable_items(self, text: str) -> List[str]:
        """Extract actionable items from general text"""
        sentences = nltk.sent_tokenize(text)
        actionable = []
        
        action_indicators = ['should', 'must', 'need to', 'recommend', 'suggest', 'advise']
        
        for sentence in sentences:
            if any(indicator in sentence.lower() for indicator in action_indicators):
                actionable.append(sentence)
        
        return actionable[:3]