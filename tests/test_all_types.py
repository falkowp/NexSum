import pytest
from pathlib import Path

from src.core.content_detector import ContentTypeDetector


def _read_test_file(name: str) -> str:
    p = Path("test_data") / f"{name}.txt"
    return p.read_text(encoding="utf-8")


@pytest.mark.parametrize("name,expected", [
    ("academic", "academic"),
    ("book", "book"),
    ("meeting", "meeting"),
    ("general", "general"),
])
def test_detect_content_types(name, expected):
    content = _read_test_file(name)
    result = ContentTypeDetector.detect_content_type(content)
    assert result.content_type == expected


def test_detect_empty_returns_general():
    result = ContentTypeDetector.detect_content_type("")
    assert result.content_type == "general"
    assert result.confidence == 0.0
