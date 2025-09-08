from typing import Optional, Dict, Any

_summarizer_app = None

def _get_app():
    global _summarizer_app
    if _summarizer_app is None:
        from src.main import SummarizerApp
        _summarizer_app = SummarizerApp()
    return _summarizer_app

def summarize_text(text: str, content_type: Optional[str] = None) -> Dict[str, Any]:
    app = _get_app()
    return app.summarize_text(text, content_type)
