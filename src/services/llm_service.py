"""Lightweight LLM service wrapper.
Supports multiple providers:
1. Ollama (LOCAL, FREE, NO REGISTRATION - best for privacy/offline)
2. Hugging Face Inference API (FREE - 1000 req/day, needs account)
3. OpenAI API (paid)
4. Groq API (free tier available)

Environment variables:
- OLLAMA_MODEL: model name (default: llama3.2:3b) - download: ollama pull llama3.2:3b
- OLLAMA_BASE_URL: base URL (default: http://localhost:11434)
- HUGGINGFACE_API_KEY: HF token (free at https://huggingface.co/settings/tokens)
- HF_MODEL: model name (default: meta-llama/Llama-3.2-3B-Instruct)
- OPENAI_API_KEY: OpenAI API key
- OPENAI_MODEL: model name (default: gpt-3.5-turbo)
- GROQ_API_KEY: Groq API key
- GROQ_MODEL: model name (default: llama-3.1-70b-versatile)
"""
from typing import Optional
import os

OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.2:3b')

HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY') or os.getenv('HF_TOKEN')
HF_MODEL = os.getenv('HF_MODEL', 'meta-llama/Llama-3.2-3B-Instruct')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.1-70b-versatile')


def generate(prompt: str, model: Optional[str] = None, max_tokens: int = 256, temperature: float = 0.2) -> str:
    """Generate text from an LLM. Tries providers in order: Ollama (local, no reg) > HuggingFace (free) > Groq > OpenAI.

    Returns the text response from the model.
    """
    # Priority 0: Ollama (local, no registration, free, private)
    try:
        result = _generate_ollama(prompt, model or OLLAMA_MODEL, max_tokens, temperature)
        if result:  # If Ollama is running and responds
            return result
    except Exception:
        # Ollama not running or not installed, try cloud options
        pass
    
    # Priority 1: HuggingFace (free, good quality)
    if HUGGINGFACE_API_KEY:
        try:
            return _generate_huggingface(prompt, model or HF_MODEL, max_tokens, temperature)
        except Exception as e:
            print(f"⚠️  HuggingFace API failed: {e}")
            # Fall through to next provider
    
    # Priority 2: Groq (free tier, very fast)
    if GROQ_API_KEY:
        try:
            return _generate_groq(prompt, model or GROQ_MODEL, max_tokens, temperature)
        except Exception as e:
            print(f"⚠️  Groq API failed: {e}")
            # Fall through to next provider
    
    # Priority 3: OpenAI (paid, high quality)
    if not OPENAI_API_KEY:
        raise RuntimeError(
            'No LLM API configured. Options:\n'
            '1. Install Ollama (local, no registration): https://ollama.com\n'
            '2. Set HUGGINGFACE_API_KEY (free 1000/day): https://huggingface.co/settings/tokens\n'
            '3. Set GROQ_API_KEY or OPENAI_API_KEY'
        )

    model = model or OPENAI_MODEL

    # Try using the openai package if available
    try:
        import openai
        openai.api_key = OPENAI_API_KEY
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        # Get assistant message
        return resp['choices'][0]['message']['content'].strip()
    except Exception:
        # Fallback to plain HTTP request
        try:
            import requests
            url = 'https://api.openai.com/v1/chat/completions'
            headers = {
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            }
            payload = {
                'model': model,
                'messages': [{"role": "user", "content": prompt}],
                'max_tokens': max_tokens,
                'temperature': temperature,
            }
            r = requests.post(url, json=payload, headers=headers, timeout=30)
            r.raise_for_status()
            data = r.json()
            return data['choices'][0]['message']['content'].strip()
        except Exception as e:
            raise RuntimeError(f'LLM call failed: {e}') from e


def _generate_ollama(prompt: str, model: str, max_tokens: int, temperature: float) -> Optional[str]:
    """Generate using Ollama (local LLM server, no registration needed).
    Returns None if Ollama is not running.
    """
    try:
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
    except Exception:
        # Ollama not running or not installed
        return None


def _generate_huggingface(prompt: str, model: str, max_tokens: int, temperature: float) -> str:
    """Generate using Hugging Face Inference API (free tier: 1000 req/day)."""
    import requests
    
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    # Format prompt for instruction models
    if 'instruct' in model.lower() or 'chat' in model.lower():
        formatted_prompt = f"<|user|>\n{prompt}\n<|assistant|>\n"
    else:
        formatted_prompt = prompt
    
    payload = {
        "inputs": formatted_prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": temperature,
            "return_full_text": False,
        }
    }
    
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    response.raise_for_status()
    
    result = response.json()
    if isinstance(result, list) and len(result) > 0:
        return result[0].get('generated_text', '').strip()
    elif isinstance(result, dict):
        return result.get('generated_text', '').strip()
    else:
        raise RuntimeError(f"Unexpected HF response format: {result}")


def _generate_groq(prompt: str, model: str, max_tokens: int, temperature: float) -> str:
    """Generate using Groq API (free tier available, very fast inference)."""
    import requests
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data['choices'][0]['message']['content'].strip()
