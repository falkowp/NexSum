from config.settings import MODEL_SETTINGS

class TextSummarizer:
    """Handle text summarization using transformer models"""
    
    def __init__(self):
        # DON'T import anything here - lazy load when needed
        self.model = None
        self._transformers_available = None
        self._torch_available = None
    
    def _check_dependencies(self):
        """Check if required dependencies are available"""
        if self._transformers_available is None:
            try:
                from transformers import pipeline
                self._transformers_available = True
            except ImportError:
                self._transformers_available = False
        
        if self._torch_available is None:
            try:
                import torch
                self._torch_available = True
            except ImportError:
                self._torch_available = False
        
        return self._transformers_available and self._torch_available
    
    def _load_model(self):
        """Lazy load the model only when needed"""
        if not self._check_dependencies():
            return None
        
        try:
            from transformers import pipeline
            import torch
            
            # Use CPU only to avoid GPU issues
            return pipeline(
                "summarization",
                model=MODEL_SETTINGS["model_name"],
                device=-1  # Force CPU
            )
        except Exception as e:
            print(f"Warning: Failed to load summarization model: {e}")
            return None
    
    def summarize(self, text: str, max_length: int = 150, min_length: int = 20) -> str:
        if self.model is None:
            self.model = self._load_model()
        
        if not self.model:
            return "Summary unavailable - model dependencies not loaded"
        
        try:
            result = self.model(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            return result[0]['summary_text']
        except Exception as e:
            return f"Summary generation failed: {e}"