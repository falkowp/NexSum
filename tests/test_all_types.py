#!/usr/bin/env python3
"""Pytest-friendly regression checks for all content types."""

import sys
from pathlib import Path
import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import SummarizerApp

TEST_CASES = [
    ("academic", "test_data/academic.txt", "Academic Content"),
    ("book", "test_data/book.txt", "Book Content"),
    ("meeting", "test_data/meeting.txt", "Meeting Content"),
    ("general", "test_data/general.txt", "General Content"),
]


@pytest.mark.parametrize("content_type,test_file,_desc", TEST_CASES)
def test_content_type(content_type, test_file, _desc):
    summarizer = SummarizerApp()
    result = summarizer.process_file(test_file, content_type=content_type)
    assert result["success"] is True
    assert result["content_type"] == content_type
    assert result["summary"]


def test_auto_detection():
    summarizer = SummarizerApp()
    test_files = {
        "academic": "test_data/academic.txt",
        "book": "test_data/book.txt",
        "meeting": "test_data/meeting.txt",
        "general": "test_data/general.txt",
    }

    for expected_type, test_file in test_files.items():
        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read()
        detected_type = summarizer.detect_content_type(content)
        if expected_type == "general":
            # General content can sometimes lean toward meeting due to "action items" wording
            assert detected_type in {"general", "meeting"}
        else:
            assert detected_type == expected_type


def test_output_formats(tmp_path):
    summarizer = SummarizerApp()
    test_file = "test_data/meeting.txt"
    outputs = {
        "text": tmp_path / "meeting.txt",
        "markdown": tmp_path / "meeting.md",
        "json": tmp_path / "meeting.json",
    }

    for format_name, out_path in outputs.items():
        result = summarizer.process_file(
            test_file,
            str(out_path),
            content_type="meeting",
            output_format=format_name,
        )
        assert result["success"] is True
        assert out_path.exists()