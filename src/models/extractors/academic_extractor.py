from .base_extractor import BaseExtractor

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

