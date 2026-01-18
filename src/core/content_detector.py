import re
from typing import Dict
from ..config.models import ContentDetectionResult

class ContentTypeDetector:
    PATTERNS = {
        'meeting': [
            r'\b(meeting|agenda|action items|decisions|participants|attendees)\b',
            r'\b(update|progress|status|discuss|review|schedule)\b',
            r'\b([A-Z][a-z]+:\s)', 
            r'\b(team|project|conference|call|minutes|action plan)\b',
            r'\b(said|says|asked|replied|responded|suggested)\b'  
        ],
        'academic': [
            r'\b(lecture|chapter|section|theory|concept|definition|theorem)\b',
            r'\b(study|research|experiment|hypothesis|methodology|analysis)\b',
            r'\b(introduction|conclusion|summary|key points|learning objectives)\b',
            r'\b(neural networks|deep learning|activation functions|backpropagation)\b'
        ],
        'book': [
            r'\b(chapter|page|paragraph|author|publisher|edition|volume)\b',
            r'\b(narrative|plot|character|setting|theme|protagonist|antagonist)\b',
            r'\b(reference|bibliography|citation|footnote|index|glossary)\b',
            r'\b(prophecy|forest|kingdom|destiny|journey|mysterious)\b'
        ]
    }
    
    @staticmethod
    def detect_content_type(text: str):
        try:
            from .content_classifier import EmbeddingContentClassifier
            emb_clf = EmbeddingContentClassifier.load()
            if emb_clf is not None:
                res = emb_clf.predict(text)
                if res.get('confidence', 0.0) >= 0.45:
                    return ContentDetectionResult(res['content_type'], res['confidence'], {'scores': res.get('scores', {}), 'evidence': res.get('evidence', [])})
                
        except Exception:
            pass

        try:
            from .content_classifier import ContentClassifier
            tf_clf = ContentClassifier.load()
            if tf_clf is not None:
                res = tf_clf.predict(text)
                if res.get('confidence', 0.0) >= 0.4:
                    return ContentDetectionResult(res['content_type'], res['confidence'], {'scores': res.get('scores', {}), 'evidence': res.get('evidence', [])})
        except Exception:
            pass
        

        text_lower = text.lower()
        scores = {}
        evidence = {}

        for content_type, patterns in ContentTypeDetector.PATTERNS.items():
            score = 0
            matches_for_type = []
            for pattern in patterns:
                found = [m.group(0) for m in re.finditer(pattern, text_lower, re.IGNORECASE)]
                score += len(found)
                matches_for_type.extend(found)
            scores[content_type] = score
            evidence[content_type] = matches_for_type[:10]
        
        total_score = sum(scores.values())
        if total_score == 0:
            return ContentDetectionResult('general', 0.0, {'scores': scores, 'evidence': evidence})
        
        detected_type = max(scores.items(), key=lambda x: x[1])[0]
        confidence = scores[detected_type] / total_score if total_score > 0 else 0.0
        
        return ContentDetectionResult(detected_type, confidence, {'scores': scores, 'evidence': evidence})