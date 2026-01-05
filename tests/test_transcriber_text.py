from unittest.mock import MagicMock
from src.transcription.transcriber import capitalize_entities


def test_capitalize_entities_uses_nlp(monkeypatch):
    text = "hello john doe world."

    # Create a fake spaCy doc with one PERSON entity for 'john doe'
    mock_ent = MagicMock()
    mock_ent.label_ = "PERSON"
    mock_ent.start_char = 6
    mock_ent.end_char = 14
    mock_ent.text = "john doe"

    mock_doc = MagicMock()
    mock_doc.ents = [mock_ent]

    # _get_nlp should return a callable that returns our mock_doc
    monkeypatch.setattr('src.transcription.transcriber._get_nlp', lambda: (lambda chunk: mock_doc))

    result = capitalize_entities(text)
    assert 'John Doe' in result
