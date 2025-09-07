import re
import nltk
from typing import Dict, List, Any, Set
from collections import defaultdict
from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    """Base class for content element extraction"""
    
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
        """Clean individual sentences by removing metadata and noise"""
        # Remove speaker labels
        sentence = re.sub(r'^[A-Z][a-z]+:\s*', '', sentence)
        # Remove bullet points and numbering
        sentence = re.sub(r'^[•\-]\s*', '', sentence)
        sentence = re.sub(r'^\d+\.\s*', '', sentence)
        # Remove action item markers
        sentence = re.sub(r'#\s*ACTION\s*ITEM', '', sentence, flags=re.IGNORECASE)
        # Remove extra whitespace
        sentence = re.sub(r'\s+', ' ', sentence).strip()
        return sentence
    
    def _extract_main_topics(self, text: str, max_topics: int = 4) -> List[str]:
        """Extract main topics from text"""
        sentences = nltk.sent_tokenize(text)
        
        # Score sentences based on importance
        scored_sentences = []
        for sentence in sentences:
            score = 0
            
            # Longer sentences are often more substantive
            if len(sentence.split()) > 8:
                score += 1
            
            # Sentences near the beginning are often topic sentences
            if sentences.index(sentence) < 3:
                score += 2
            
            # Sentences with key topic indicators
            topic_indicators = ['key', 'important', 'main', 'primary', 'focus', 'objective']
            if any(indicator in sentence.lower() for indicator in topic_indicators):
                score += 2
            
            scored_sentences.append((sentence, score))
        
        # Sort by score and return top sentences
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        return [sentence for sentence, score in scored_sentences[:max_topics]]

