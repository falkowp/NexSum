from transformers import pipeline
import torch
from config.settings import MODEL_SETTINGS

class TextSummarizer:
    """Handle text summarization using transformer models"""
    
    def __init__(self):
        self.model = self._load_model()
    
    def _load_model(self):
        try:
            return pipeline(
                "summarization",
                model=MODEL_SETTINGS["model_name"],
                device=0 if torch.cuda.is_available() else -1
            )
        except Exception as e:
            raise Exception(f"Failed to load summarization model: {e}")
    
    def summarize(self, text: str, max_length: int = 150, min_length: int = 20) -> str:
        if not self.model:
            return "Summary unavailable - model not loaded"
        
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