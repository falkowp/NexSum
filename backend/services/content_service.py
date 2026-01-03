from typing import Dict, Any
from src.core.content_detector import ContentTypeDetector


def detect_content_type(text: str) -> Dict[str, Any]:
    """Detect content type and return a serializable dict with evidence."""
    res = ContentTypeDetector.detect_content_type(text)
    return {
        "content_type": res.content_type,
        "confidence": res.confidence,
        "features": res.features,
    }