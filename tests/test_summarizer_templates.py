import sys, os
# Ensure src package is on path so `config.*` imports resolve
sys.path.insert(0, os.path.abspath('src'))

from src.models.summarizers.summarizer import TextSummarizer


def test_mock_summary_includes_type_header():
    ts = TextSummarizer()
    # force mock path by disabling dependencies
    ts._dependencies_available = False

    text = "This is a meeting. We discussed budgets. We decided to allocate more resources."
    res = ts.summarize(text, content_type='meeting')
    assert '[MEETING SUMMARY]' in res

    text2 = "A chapter about characters and themes. The protagonist travels." 
    res2 = ts.summarize(text2, content_type='book')
    assert '[BOOK SUMMARY]' in res2
