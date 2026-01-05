from pathlib import Path
import tempfile
import os
from src.core.content_classifier import ContentClassifier
from src.core.content_detector import ContentTypeDetector


def test_train_and_predict(tmp_path):
    # Use existing test_data folder available at project root
    data_dir = Path('test_data')
    cc = ContentClassifier()
    cc.train(data_dir)
    # After training, model file should exist
    model_loaded = ContentClassifier.load()
    assert model_loaded is not None

    # Quick prediction
    s = 'In the meeting we decided on action items and assigned tasks to participants.'
    pred = model_loaded.predict(s)
    assert 'content_type' in pred
    assert pred['content_type'] in ('meeting', 'general', 'academic', 'book')

    # Ensure detector uses classifier (detect_content_type will prefer classifier)
    res = ContentTypeDetector.detect_content_type(s)
    assert res.content_type == pred['content_type']
    # cleanup model
    model_path = Path(__file__).resolve().parents[1] / 'src' / 'models' / 'content_classifier.joblib'
    if model_path.exists():
        os.remove(model_path)
