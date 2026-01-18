import os
from src.config.settings import MODEL_SETTINGS

MAX_TOKENS = 400

class TextSummarizer:
    
    def __init__(self):
        self.model = None
        self._use_llm = self._check_ollama_available()
        
        if not self._use_llm:
            self._dependencies_available = self._check_dependencies()
            if self._dependencies_available:
                self.model = self._load_model()
        else:
            self._dependencies_available = False
    
    def _check_ollama_available(self) -> bool:
        try:
            import requests
            ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
            response = requests.get(f"{ollama_url}/api/tags", timeout=2)
            return response.status_code == 200
        except Exception:
            return False
    
    def _check_dependencies(self):
        try:
            import importlib
            importlib.import_module('transformers')
            importlib.import_module('torch')
            return True
        except ImportError:
            return False
    
    def _load_model(self):
        try:
            import torch
            torch._dynamo.config.suppress_errors = True
            os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
            
            from transformers import pipeline
            return pipeline(
                "summarization",
                model=MODEL_SETTINGS["model_name"],
                device=-1,  
                torch_dtype=torch.float32  
            )
        except Exception as e:
            print(f"Could not load summarization model: {e}")
            return None
    
    def summarize(self, text: str, content_type: str = None, max_length: int = 220, min_length: int = 80) -> str:
        
        from src.config.output_config import OutputConfig

        template = None
        if content_type:
            template = OutputConfig.get_template(content_type)

        prompt = template.format(text=text) if template else text

        try:
            from src.services import llm_service
            llm_resp = llm_service.generate(prompt, max_tokens=MAX_TOKENS)
            return llm_resp
        except RuntimeError as e:
            print(f" Ollama not available: {e}")
            print("Falling back to local transformer model...")
        except Exception as e:
            print(f"LLM call failed ({e}), falling back to local model")

        needs_chunking = len(text.split()) > 800
        
        if self._dependencies_available and self.model:
            try:
                if needs_chunking:
                    return self._chunk_and_summarize(prompt, max_length, min_length)
                else:
                    result = self.model(
                        prompt,
                        max_length=max_length,
                        min_length=min_length,
                        do_sample=False
                    )
                    return result[0]['summary_text']
            except Exception as e:
                print(f" Local summarization failed ({e}), using fallback mock summary")
                pass

        return self._create_mock_summary(text, content_type)
    
    def _chunk_and_summarize(self, text: str, max_length: int, min_length: int) -> str:
        """Split long text into chunks and summarize each, then combine."""
        try:
            from nltk.tokenize import sent_tokenize
            sentences = sent_tokenize(text)
        except:
            sentences = text.split('. ')
        
        chunks = []
        current_chunk = []
        current_words = 0
        
        for sentence in sentences:
            sentence_words = len(sentence.split())
            if current_words + sentence_words > 400 and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_words = sentence_words
            else:
                current_chunk.append(sentence)
                current_words += sentence_words
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        chunk_summaries = []
        for chunk in chunks:
            try:
                result = self.model(
                    chunk,
                    max_length=min(150, max_length // len(chunks)),
                    min_length=30,
                    do_sample=False
                )
                chunk_summaries.append(result[0]['summary_text'])
            except Exception:
                continue
        
        combined = ' '.join(chunk_summaries)
        
        if len(combined.split()) > max_length:
            try:
                result = self.model(
                    combined,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False
                )
                return result[0]['summary_text']
            except Exception:
                return combined[:max_length * 5]  # Rough character limit
        
        return combined

    def _create_mock_summary(self, text: str, content_type: str = None) -> str:
        header = f"[{content_type.upper()} SUMMARY] " if content_type else "[MOCK SUMMARY] "
        sentences = text.split('. ')
        if len(sentences) > 3:
            summary = '. '.join(sentences[:2]) + '...'
        else:
            summary = text[:100] + '...' if len(text) > 100 else text
        return f"{header}{summary}"