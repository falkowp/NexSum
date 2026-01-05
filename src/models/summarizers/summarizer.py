import os
from src.config.settings import MODEL_SETTINGS

MAX_TOKENS = 400  # cap LLM responses for fuller summaries without runaway length

class TextSummarizer:
    """Handle text summarization - with proper fallback"""
    
    def __init__(self):
        self.model = None
        # Check if any LLM API is available - if yes, skip loading local model to save memory
        # Note: Ollama doesn't need env var, we'll try it anyway in generate()
        self._use_llm = (
            self._check_ollama_available() or
            os.getenv("HUGGINGFACE_API_KEY") is not None or
            os.getenv("HF_TOKEN") is not None or
            os.getenv("GROQ_API_KEY") is not None or
            os.getenv("OPENAI_API_KEY") is not None
        )
        
        if not self._use_llm:
            # Only load local model if no API key is set
            self._dependencies_available = self._check_dependencies()
            if self._dependencies_available:
                self.model = self._load_model()
        else:
            self._dependencies_available = False
    
    def _check_ollama_available(self) -> bool:
        """Check if Ollama is running locally."""
        try:
            import requests
            ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
            response = requests.get(f"{ollama_url}/api/tags", timeout=2)
            return response.status_code == 200
        except Exception:
            return False
    
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
            # Disable torch compile to avoid Meta tensor errors
            import torch
            torch._dynamo.config.suppress_errors = True
            os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
            
            from transformers import pipeline
            return pipeline(
                "summarization",
                model=MODEL_SETTINGS["model_name"],
                device=-1,  # Force CPU
                torch_dtype=torch.float32  # Explicit dtype to avoid compilation issues
            )
        except Exception as e:
            print(f"⚠️  Could not load summarization model: {e}")
            return None
    
    def summarize(self, text: str, content_type: str = None, max_length: int = 220, min_length: int = 80) -> str:
        """Generate a summary. If a template for content_type exists, apply it to the prompt.
        """
        from src.config.output_config import OutputConfig

        template = None
        if content_type:
            template = OutputConfig.get_template(content_type)

        prompt = template.format(text=text) if template else text

        # PRIORITY 1: Use LLM API if configured (faster, better quality, follows templates)
        # This includes Ollama (local), HuggingFace, Groq, and OpenAI
        try:
            from src.services import llm_service
            # Always try LLM service - it will check Ollama first, then API keys
            llm_resp = llm_service.generate(prompt, max_tokens=MAX_TOKENS)
            return llm_resp
        except RuntimeError as e:
            # No LLM available (neither Ollama nor API keys)
            if "No LLM" in str(e):
                print(f"⚠️  {e}")
            pass
        except Exception as e:
            print(f"⚠️  LLM API call failed ({e}), falling back to local model")
            pass

        # PRIORITY 2: Use local model if available (for users without API key)
        # For very long texts, chunk them to get better coverage
        needs_chunking = len(text.split()) > 800
        
        if self._dependencies_available and self.model:
            try:
                # For long texts, use chunking to get better coverage
                if needs_chunking:
                    return self._chunk_and_summarize(prompt, max_length, min_length)
                else:
                    result = self.model(
                        prompt,
                        max_length=max_length,
                        min_length=min_length,
                        do_sample=False
                    )
                    # The summarization model returns a single result with 'summary_text'
                    return result[0]['summary_text']
            except Exception as e:
                print(f"⚠️  Local summarization failed ({e}), using fallback mock summary")
                # Fall through to mock summary instead of returning error message
                pass

        # Fallback to mock summary when neither LLM nor local model are available
        return self._create_mock_summary(text, content_type)
    
    def _chunk_and_summarize(self, text: str, max_length: int, min_length: int) -> str:
        """Split long text into chunks and summarize each, then combine."""
        try:
            from nltk.tokenize import sent_tokenize
            sentences = sent_tokenize(text)
        except:
            # Fallback split
            sentences = text.split('. ')
        
        # Group sentences into chunks of ~400 words
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
        
        # Summarize each chunk
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
                # Skip failed chunks
                continue
        
        # Combine chunk summaries
        combined = ' '.join(chunk_summaries)
        
        # If combined is still too long, summarize again
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
        """Create a simple mock summary when dependencies aren't available.
        Add a header that reflects the selected content type for clarity.
        """
        header = f"[{content_type.upper()} SUMMARY] " if content_type else "[MOCK SUMMARY] "
        sentences = text.split('. ')
        if len(sentences) > 3:
            summary = '. '.join(sentences[:2]) + '...'
        else:
            summary = text[:100] + '...' if len(text) > 100 else text
        return f"{header}{summary}"