"""Lightweight LLM service wrapper using Ollama.

Ollama provides:
- Local LLM inference (runs on your machine)
- No registration or API keys needed
- Complete privacy - your data stays local
- Free and open source

Setup:
1. Install Ollama: https://ollama.com
2. Pull a model: ollama pull llama3.2:3b
3. Start using (Ollama service starts automatically)

Environment variables:
- OLLAMA_MODEL: model name (default: llama3.2:3b)
- OLLAMA_BASE_URL: base URL (default: http://localhost:11434)
"""
from typing import Optional
import os

OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.2:3b')


def generate(prompt: str, model: Optional[str] = None, max_tokens: int = 256, temperature: float = 0.2) -> str:
    """Generate text using Ollama local LLM.

    Args:
        prompt: The text prompt to send to the model
        model: Model name (default: from OLLAMA_MODEL env var)
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature (0.0-1.0)

    Returns:
        Generated text response from the model

    Raises:
        RuntimeError: If Ollama is not running or model is not available
    """
    model = model or OLLAMA_MODEL
    
    try:
        result = _generate_ollama(prompt, model, max_tokens, temperature)
        if result:
            return result
        else:
            raise RuntimeError("Ollama returned empty response")
    except Exception as e:
        raise RuntimeError(
            f'Ollama LLM call failed: {e}\n\n'
            'Make sure:\n'
            '1. Ollama is installed: https://ollama.com\n'
            '2. Ollama service is running (should start automatically)\n'
            f'3. Model "{model}" is downloaded: ollama pull {model}\n'
            '4. Try: ollama list (to see available models)'
        ) from e


def _generate_ollama(prompt: str, model: str, max_tokens: int, temperature: float) -> Optional[str]:
    """Generate using Ollama local LLM server."""
    import requests
    
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        }
    }
    
    response = requests.post(url, json=payload, timeout=90)
    response.raise_for_status()
    result = response.json()
    return result.get('response', '').strip()
