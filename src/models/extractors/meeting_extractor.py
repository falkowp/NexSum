from .base_extractor import BaseExtractor
import re
import nltk
from typing import Dict, List, Any, Set
from collections import defaultdict
from abc import ABC, abstractmethod

class MeetingElementsExtractor(BaseExtractor):
    
    def extract(self, text: str) -> Dict[str, Any]:
        speakers = self._extract_speakers(text)
        action_items = self._extract_action_items(text)
        decisions = self._extract_decisions(text)
        key_points = self._extract_main_topics(text)
        
        return {
            "speakers": speakers,
            "action_items": action_items,
            "decisions": decisions,
            "key_points": key_points
        }
    
    def _extract_speakers(self, text: str) -> List[str]:
        speaker_pattern = r'\b([A-Z][a-z]+)(?=:)'
        all_speakers = re.findall(speaker_pattern, text)
        
        non_speaker_words = {'items', 'participants', 'decisions', 'action', 'meeting', 
                            'the', 'major', 'characters', 'key', 'review', 'status'}
        speakers = [s for s in set(all_speakers) if s.lower() not in non_speaker_words]
        
        return speakers[:10]  
    
    def _extract_action_items(self, text: str) -> List[str]:
        sentences = nltk.sent_tokenize(text)
        action_items = []
        
        for sentence in sentences:
            sentence_clean = self._clean_sentence(sentence)
            if len(sentence_clean.split()) < 4: 
                continue
                
            sentence_lower = sentence_clean.lower()
            
            action_indicators = [
                r'\b(i\'ll|i will|we\'ll|we will|will\s+[^.!?]*\b(check|investigate|review|test|fix|implement|complete))\b',
                r'\b(need to|must|should|action item|task|assign)\b',
                r'\b(by [a-z]+day|by \d+|deadline|due)\b'
            ]
            
            is_action = (any(re.search(pattern, sentence_lower) for pattern in action_indicators) and
                        '?' not in sentence_clean and
                        self._is_valid_action_item(sentence_clean))
            
            if is_action:
                action_items.append(sentence_clean)
        
        return action_items[:5]
    
    def _extract_decisions(self, text: str) -> List[str]:
        sentences = nltk.sent_tokenize(text)
        decisions = []
        
        for sentence in sentences:
            sentence_clean = self._clean_sentence(sentence)
            if len(sentence_clean.split()) < 4:  
                continue
                
            sentence_lower = sentence_clean.lower()
            
            decision_indicators = [
                r'\b(decided|agreed|concluded|decision|consensus|vote)\b',
                r'\b(schedule|meet|thursday|friday|next week)\b'
            ]
            
            is_decision = any(re.search(pattern, sentence_lower) for pattern in decision_indicators)
            
            if is_decision:
                decisions.append(sentence_clean)
        
        return decisions[:3]
    
    def _is_valid_action_item(self, sentence: str) -> bool:
        if len(sentence.split()) < 4: 
            return False
        
        sentence_lower = sentence.lower()
        
        if '?' in sentence or any(word in sentence_lower for word in ['maybe', 'perhaps', 'possibly']):
            return False
        
        action_verbs = ['will', 'shall', 'should', 'must', 'need to', 'going to', "i'll", "we'll"]
        time_references = ['by', 'until', 'before', 'after', 'next', 'tomorrow', 'friday', 'wednesday']
        
        has_action_verb = any(verb in sentence_lower for verb in action_verbs)
        has_time_reference = any(time in sentence_lower for time in time_references)
        
        return has_action_verb or has_time_reference

