import re
import nltk
from typing import Dict, List, Any, Set
from collections import defaultdict
from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    
    def __init__(self):
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
    
    @abstractmethod
    def extract(self, text: str) -> Dict[str, Any]:
        pass
    
    def _clean_sentence(self, sentence: str) -> str:
        sentence = re.sub(r'^[A-Z][a-z]+:\s*', '', sentence)
        sentence = re.sub(r'^[•\-]\s*', '', sentence)
        sentence = re.sub(r'^\d+\.\s*', '', sentence)
        sentence = re.sub(r'#\s*ACTION\s*ITEM', '', sentence, flags=re.IGNORECASE)
        sentence = re.sub(r'\s+', ' ', sentence).strip()
        return sentence
    
    def _extract_main_topics(self, text: str, max_topics: int = 4) -> List[str]:
        sentences = nltk.sent_tokenize(text)
        
        scored_sentences = []
        for sentence in sentences:
            score = 0
            
            if len(sentence.split()) > 8:
                score += 1
            
            if sentences.index(sentence) < 3:
                score += 2
            
            topic_indicators = ['key', 'important', 'main', 'primary', 'focus', 'objective']
            if any(indicator in sentence.lower() for indicator in topic_indicators):
                score += 2
            
            scored_sentences.append((sentence, score))
        
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        return [sentence for sentence, score in scored_sentences[:max_topics]]

