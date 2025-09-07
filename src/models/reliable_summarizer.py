import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import re
from collections import defaultdict

class ReliableTextSummarizer:
    """High-quality summarizer that works without external dependencies"""
    
    def __init__(self):
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
    
    def summarize(self, text: str, max_length: int = 150, min_length: int = 20) -> str:
        """Create intelligent extractive summary"""
        try:
            # Clean text
            text = re.sub(r'\s+', ' ', text).strip()
            if len(text) < 100:
                return text
            
            sentences = sent_tokenize(text)
            if len(sentences) <= 2:
                return text
            
            # Score sentences based on importance
            scored_sentences = []
            word_freq = self._calculate_word_frequency(text)
            
            for i, sentence in enumerate(sentences):
                score = 0
                
                # First sentences are often important
                if i < 2:
                    score += 2
                
                # Longer sentences often contain more information
                if len(word_tokenize(sentence)) > 8:
                    score += 1
                
                # Sentences with important words
                for word in word_tokenize(sentence.lower()):
                    if word in word_freq and len(word) > 4:
                        score += word_freq[word]
                
                scored_sentences.append((sentence, score))
            
            # Sort by score and take top sentences
            scored_sentences.sort(key=lambda x: x[1], reverse=True)
            
            # Build summary
            summary_sentences = []
            total_length = 0
            
            for sentence, score in scored_sentences[:4]:  # Take top 4
                if total_length + len(sentence) <= max_length:
                    summary_sentences.append(sentence)
                    total_length += len(sentence)
            
            # Ensure we have enough content
            if total_length < min_length and len(summary_sentences) < 2:
                summary_sentences = sentences[:2]
            
            summary = ' '.join(summary_sentences)
            
            # Trim if necessary
            if len(summary) > max_length:
                summary = summary[:max_length].rsplit('.', 1)[0] + '.'
            
            return summary
            
        except Exception as e:
            # Fallback: first few sentences
            sentences = sent_tokenize(text)
            return ' '.join(sentences[:2]) if len(sentences) > 1 else text[:max_length]
    
    def _calculate_word_frequency(self, text: str) -> dict:
        """Calculate word frequency excluding stopwords"""
        words = word_tokenize(text.lower())
        stop_words = set(nltk.corpus.stopwords.words('english'))
        word_freq = defaultdict(int)
        
        for word in words:
            if word.isalpha() and word not in stop_words and len(word) > 3:
                word_freq[word] += 1
        
        return dict(word_freq)

# Use this as the default summarizer
TextSummarizer = ReliableTextSummarizer