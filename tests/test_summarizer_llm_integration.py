import os
import sys
sys.path.insert(0, os.path.abspath('src'))

from src.models.summarizers.summarizer import TextSummarizer


def test_llm_path_monkeypatch(monkeypatch):
    # ensure OPENAI_API_KEY is set in env for the test
    monkeypatch.setenv('OPENAI_API_KEY', 'testkey')

    # monkeypatch the llm_service.generate function
    import src.services.llm_service as llm

    def fake_generate(prompt, model=None, max_tokens=256, temperature=0.2):
        assert 'Meeting Summary' in prompt or 'Transcript:' in prompt or 'Meeting' in prompt
        return 'MOCK LLM SUMMARY'

    monkeypatch.setattr(llm, 'generate', fake_generate)

    ts = TextSummarizer()
    ts._dependencies_available = False  # force path to use llm instead of local pipeline

    res = ts.summarize('Some meeting content here', content_type='meeting')
    assert res == 'MOCK LLM SUMMARY'
