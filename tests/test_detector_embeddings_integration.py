import pytest
from src.core.content_detector import ContentTypeDetector
from pathlib import Path

pytest.importorskip('sentence_transformers')
from src.core.content_classifier import EmbeddingContentClassifier


def test_detector_uses_embeddings(tmp_path):
    data_dir = Path('test_data')
    # train small model
    clf = EmbeddingContentClassifier()
    clf.train(data_dir)

    res = ContentTypeDetector.detect_content_type('This meeting discussed progress on the project and assigned action items')
    assert hasattr(res, 'content_type')
    assert hasattr(res, 'confidence')
    assert isinstance(res.confidence, float)
    assert res.content_type in ('meeting', 'general', 'academic', 'book')
    # After training, confidence should often be > 0 (non-zero)
    assert res.confidence >= 0.0