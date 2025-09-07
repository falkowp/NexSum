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

class MeetingElementsExtractor(BaseExtractor):
    """Extract meeting-specific elements"""
    
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
        """Extract speaker names from meeting text"""
        speaker_pattern = r'\b([A-Z][a-z]+)(?=:)'
        all_speakers = re.findall(speaker_pattern, text)
        
        # Filter out non-name words
        non_speaker_words = {'items', 'participants', 'decisions', 'action', 'meeting', 
                            'the', 'major', 'characters', 'key', 'review', 'status'}
        speakers = [s for s in set(all_speakers) if s.lower() not in non_speaker_words]
        
        return speakers[:10]  # Limit to top 10 speakers
    
    def _extract_action_items(self, text: str) -> List[str]:
        """Extract action items from meeting text"""
        sentences = nltk.sent_tokenize(text)
        action_items = []
        
        for sentence in sentences:
            sentence_clean = self._clean_sentence(sentence)
            if len(sentence_clean.split()) < 4:  # Skip very short sentences
                continue
                
            sentence_lower = sentence_clean.lower()
            
            # Action item indicators
            action_indicators = [
                r'\b(i\'ll|i will|we\'ll|we will|will\s+[^.!?]*\b(check|investigate|review|test|fix|implement|complete))\b',
                r'\b(need to|must|should|action item|task|assign)\b',
                r'\b(by [a-z]+day|by \d+|deadline|due)\b'
            ]
            
            # Check if sentence contains action indicators AND is not a question
            is_action = (any(re.search(pattern, sentence_lower) for pattern in action_indicators) and
                        '?' not in sentence_clean and
                        self._is_valid_action_item(sentence_clean))
            
            if is_action:
                action_items.append(sentence_clean)
        
        return action_items[:5]
    
    def _extract_decisions(self, text: str) -> List[str]:
        """Extract decisions from meeting text"""
        sentences = nltk.sent_tokenize(text)
        decisions = []
        
        for sentence in sentences:
            sentence_clean = self._clean_sentence(sentence)
            if len(sentence_clean.split()) < 4:  # Skip very short sentences
                continue
                
            sentence_lower = sentence_clean.lower()
            
            # Decision indicators
            decision_indicators = [
                r'\b(decided|agreed|concluded|decision|consensus|vote)\b',
                r'\b(schedule|meet|thursday|friday|next week)\b'
            ]
            
            is_decision = any(re.search(pattern, sentence_lower) for pattern in decision_indicators)
            
            if is_decision:
                decisions.append(sentence_clean)
        
        return decisions[:3]
    
    def _is_valid_action_item(self, sentence: str) -> bool:
        """Check if a sentence is a valid action item"""
        if len(sentence.split()) < 4:  # Too short
            return False
        
        sentence_lower = sentence.lower()
        
        # Exclude questions and uncertain statements
        if '?' in sentence or any(word in sentence_lower for word in ['maybe', 'perhaps', 'possibly']):
            return False
        
        # Must contain action indicators
        action_verbs = ['will', 'shall', 'should', 'must', 'need to', 'going to', "i'll", "we'll"]
        time_references = ['by', 'until', 'before', 'after', 'next', 'tomorrow', 'friday', 'wednesday']
        
        has_action_verb = any(verb in sentence_lower for verb in action_verbs)
        has_time_reference = any(time in sentence_lower for time in time_references)
        
        return has_action_verb or has_time_reference

class AcademicElementsExtractor(BaseExtractor):
    """Extract academic-specific elements"""
    
    def extract(self, text: str) -> Dict[str, Any]:
        key_concepts = self._extract_key_concepts(text)
        learning_objectives = self._extract_learning_objectives(text)
        main_topics = self._extract_main_topics(text)
        key_definitions = self._extract_key_definitions(text)
        
        return {
            "key_concepts": key_concepts,
            "learning_objectives": learning_objectives,
            "main_topics": main_topics,
            "key_definitions": key_definitions
        }
    
    def _extract_key_concepts(self, text: str) -> List[str]:
        """Extract key concepts from academic text"""
        words = nltk.word_tokenize(text.lower())
        word_freq = defaultdict(int)
        
        # Academic stop words to exclude
        academic_stop_words = {
            'networks', 'functions', 'learning', 'data', 'systems', 'applications', 
            'image', 'recognition', 'language', 'processing', 'lecture', 'chapter'
        }
        
        for word in words:
            if (word.isalpha() and len(word) > 5 and
                word not in academic_stop_words and
                word not in nltk.corpus.stopwords.words('english')):
                word_freq[word] += 1
        
        return [word for word, count in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:8]]
    
    def _extract_learning_objectives(self, text: str) -> List[str]:
        """Extract learning objectives from academic text"""
        objectives = set()  # Use set to avoid duplicates
        
        # Improved pattern matching
        objective_patterns = [
            r'learning objectives?[:\n]\s*([^\.]+?)(?=\.|\n\n|\n[A-Z]|$)',
            r'objectives?[:\n]\s*([^\.]+?)(?=\.|\n\n|\n[A-Z]|$)',
            r'goals?[:\n]\s*([^\.]+?)(?=\.|\n\n|\n[A-Z]|$)',
        ]
        
        for pattern in objective_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                # Split by lines and clean
                lines = match.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and any(keyword in line.lower() for keyword in 
                                ['understand', 'learn', 'study', 'know', 'objective', 'goal', 'able to']):
                        # Clean up the objective text
                        clean_obj = re.sub(r'Key concepts.*', '', line)  # Remove trailing text
                        clean_obj = clean_obj.strip()
                        if clean_obj:
                            objectives.add(clean_obj)
        
        # Also look for bullet points with objectives
        bullet_pattern = r'(?:^|\n)\s*[-•*]\s*([^\n]+?)(?=\n\s*[-•*]|\n\n|$)'
        bullet_matches = re.findall(bullet_pattern, text, re.IGNORECASE)
        for match in bullet_matches:
            if any(keyword in match.lower() for keyword in 
                ['understand', 'learn', 'study', 'know', 'objective']):
                objectives.add(match.strip())
        
        return list(objectives)[:5] if objectives else ["Learning objectives not explicitly stated"]

    def _extract_key_definitions(self, text: str) -> List[str]:
        """Extract key definitions from academic text"""
        sentences = nltk.sent_tokenize(text)
        definitions = []
        
        definition_indicators = ['defined as', 'means that', 'refers to', 'is called', 'known as']
        
        for sentence in sentences:
            if any(indicator in sentence.lower() for indicator in definition_indicators):
                definitions.append(sentence)
        
        return definitions[:3]

class BookElementsExtractor(BaseExtractor):
    """Extract book-specific elements"""
    
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
        """Extract key characters from book text"""
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
                    
                    # Check context for character indicators
                    context_words = words[max(0, i-2):min(len(words), i+3)]
                    context_text = ' '.join(context_words).lower()
                    
                    if any(indicator in context_text for indicator in 
                          ['said', 'asked', 'replied', 'stood', 'walked', 'looked', 'character']):
                        characters.add(word)
        
        # Look for character lists
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
        """Extract major themes from book text"""
        sentences = nltk.sent_tokenize(text)
        themes = []
        theme_keywords = ['theme', 'motif', 'symbol', 'meaning', 'represents', 'symbolism']
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in theme_keywords):
                themes.append(sentence)
        
        return themes[:3]
    
    def _extract_plot_points(self, text: str) -> List[str]:
        """Extract key plot points from book text"""
        sentences = nltk.sent_tokenize(text)
        plot_points = []
        plot_keywords = ['discovery', 'encounter', 'decision', 'journey', 'danger', 'conflict', 'prophecy']
        
        for sentence in sentences:
            if (len(sentence.split()) > 8 and
                any(keyword in sentence.lower() for keyword in plot_keywords)):
                plot_points.append(sentence)
        
        return plot_points[:4]
    
    def _extract_setting(self, text: str) -> List[str]:
        """Extract setting descriptions from book text"""
        sentences = nltk.sent_tokenize(text)
        settings = []
        setting_keywords = ['forest', 'castle', 'city', 'village', 'kingdom', 'island', 'mountain']
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in setting_keywords):
                settings.append(sentence)
        
        return settings[:2]

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