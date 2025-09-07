from config.settings import MODEL_SETTINGS

class TextSummarizer:
    """Handle text summarization - with proper fallback"""
    
    def __init__(self):
        self.model = None
        self._dependencies_available = self._check_dependencies()
        if self._dependencies_available:
            self.model = self._load_model()
    
    def _check_dependencies(self):
        """Check if transformers and torch are available"""
        try:
            import importlib
            importlib.import_module('transformers')
            importlib.import_module('torch')
            return True
        except ImportError:
            return False
    
    def _load_model(self):
        """Load the summarization model"""
        try:
            from transformers import pipeline
            return pipeline(
                "summarization",
                model=MODEL_SETTINGS["model_name"],
                device=-1  # Force CPU
            )
        except Exception as e:
            print(f"⚠️  Could not load summarization model: {e}")
            return None
    
    def summarize(self, text: str, max_length: int = 150, min_length: int = 20) -> str:
        if not self._dependencies_available:
            return self._create_mock_summary(text)
        
        if not self.model:
            return "Summary unavailable - model failed to load"
        
        try:
            result = self.model(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            return result[0]['summary_text']
        except Exception as e:
            return f"Summary generation error: {e}"
    
    def _create_mock_summary(self, text: str) -> str:
        """Create a simple mock summary when dependencies aren't available"""
        sentences = text.split('. ')
        if len(sentences) > 3:
            summary = '. '.join(sentences[:2]) + '...'
        else:
            summary = text[:100] + '...' if len(text) > 100 else text
        return f"[MOCK SUMMARY] {summary}"