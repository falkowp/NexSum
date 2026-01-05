import pytest
from pathlib import Path

pytest.importorskip('sentence_transformers')

from src.core.content_classifier import EmbeddingContentClassifier


def test_train_and_predict(tmp_path):
    data_dir = Path('test_data')
    clf = EmbeddingContentClassifier()
    # Train on small test_data dir — should not error
    clf.train(data_dir)

    res = clf.predict('This meeting reviewed project status and decided on next actions')
    assert 'content_type' in res
    assert 'confidence' in res
    assert isinstance(res['confidence'], float)
    assert 'scores' in res
    assert 'evidence' in res
    # Evidence should include one of the training examples when train_texts were saved
    if hasattr(clf, 'train_texts') and clf.train_texts:
        assert any(e in ' '.join(clf.train_texts) or e == t for e in res['evidence'] for t in clf.train_texts)
