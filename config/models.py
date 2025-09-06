from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ProcessingResult:
    content_type: str
    summary: str
    metadata: Dict[str, Any]
    raw_text: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "content_type": self.content_type,
            "summary": self.summary,
            **self.metadata
        }

@dataclass
class ContentDetectionResult:
    content_type: str
    confidence: float
    features: Dict[str, Any]