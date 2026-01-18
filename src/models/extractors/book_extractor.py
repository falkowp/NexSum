from .base_extractor import BaseExtractor
import re
import nltk
from typing import Dict, List, Any, Set
from collections import defaultdict
from abc import ABC, abstractmethod

class BookElementsExtractor(BaseExtractor):
    
    def extract(self, text: str) -> Dict[str, Any]:
        key_characters = self._extract_key_characters(text)
        major_themes = self._extract_major_themes(text)
        plot_points = self._extract_plot_points(text)
        setting = self._extract_setting(text)
        
        return {
            "key_characters": key_characters,
            "major_themes": major_themes,
            "plot_points": plot_points,
            "setting": setting
        }
    
    def _extract_key_characters(self, text: str) -> List[str]:
        characters: Set[str] = set()
        non_character_words = {
            'the', 'chapter', 'page', 'author', 'key', 'major', 'characters', 
            'theme', 'plot', 'great', 'transformation', 'forest', 'kingdom',
            'destiny', 'journey', 'ancient', 'prophecy', 'symbolism', 'stability'
        }
        
        sentences = nltk.sent_tokenize(text)
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            for i, word in enumerate(words):
                if (word.istitle() and len(word) > 2 and 
                    word.lower() not in non_character_words and
                    word.isalpha()):
                    
                    context_words = words[max(0, i-2):min(len(words), i+3)]
                    context_text = ' '.join(context_words).lower()
                    
                    if any(indicator in context_text for indicator in 
                          ['said', 'asked', 'replied', 'stood', 'walked', 'looked', 'character']):
                        characters.add(word)
        
        character_patterns = [
            r'characters?[:\n]\s*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'key characters?[:\n]\s*(.*?)(?=\n\n|\n[A-Z]|$)'
        ]
        
        for pattern in character_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                names = re.findall(r'\b([A-Z][a-z]+)\b', match)
                for name in names:
                    if name.lower() not in non_character_words:
                        characters.add(name)
        
        return list(characters)[:5]
    
    def _extract_major_themes(self, text: str) -> List[str]:
        sentences = nltk.sent_tokenize(text)
        themes = []
        theme_keywords = ['theme', 'motif', 'symbol', 'meaning', 'represents', 'symbolism']
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in theme_keywords):
                themes.append(sentence)
        
        return themes[:3]
    
    def _extract_plot_points(self, text: str) -> List[str]:
        sentences = nltk.sent_tokenize(text)
        plot_points = []
        plot_keywords = ['discovery', 'encounter', 'decision', 'journey', 'danger', 'conflict', 'prophecy']
        
        for sentence in sentences:
            if (len(sentence.split()) > 8 and
                any(keyword in sentence.lower() for keyword in plot_keywords)):
                plot_points.append(sentence)
        
        return plot_points[:4]
    
    def _extract_setting(self, text: str) -> List[str]:
        sentences = nltk.sent_tokenize(text)
        settings = []
        setting_keywords = ['forest', 'castle', 'city', 'village', 'kingdom', 'island', 'mountain']
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in setting_keywords):
                settings.append(sentence)
        
        return settings[:2]

