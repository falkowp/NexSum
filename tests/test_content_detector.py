from src.core.content_detector import ContentTypeDetector


def test_detect_meeting():
    text = "This meeting agenda includes action items and participants will review progress and decisions"
    res = ContentTypeDetector.detect_content_type(text)
    assert res.content_type == 'meeting'
    assert res.confidence > 0
    assert 'action items' in ' '.join(res.features.get('evidence', {}).get('meeting', []))


def test_detect_academic():
    text = "In this lecture we discuss the theorem and the methodology of the experiment"
    res = ContentTypeDetector.detect_content_type(text)
    assert res.content_type == 'academic'
    assert res.confidence > 0


def test_detect_book():
    text = "The chapter describes the hero's journey and the narrative's theme and plot"
    res = ContentTypeDetector.detect_content_type(text)
    assert res.content_type == 'book'
    assert res.confidence > 0
