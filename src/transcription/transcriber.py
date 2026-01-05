import os
import re
import io
import numpy as np
from pydub import AudioSegment

# Optional backends: faster-whisper (preferred on GPU), openai-whisper fallback
USE_FASTER = False
_faster_available = False
try:
    from faster_whisper import WhisperModel  # type: ignore
    _faster_available = True
except Exception:
    _faster_available = False

try:
    import torch
    _cuda_available = torch.cuda.is_available()
except Exception:
    _cuda_available = False

# Lazy-loaded models
_faster_model = None
_whisper_model = None

# Load spaCy and other text utilities lazily to avoid heavy imports if unused
_nlp = None

def _get_nlp():
    global _nlp
    if _nlp is None:
        import spacy
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


def convert_to_wav_16k_mono(audio_bytes: bytes) -> AudioSegment:
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)
    return audio


def audiosegment_to_np(audio: AudioSegment) -> np.ndarray:
    samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
    samples /= np.iinfo(audio.array_type).max
    return samples


def _load_faster_model():
    global _faster_model
    if _faster_model is None:
        model_name = os.environ.get("WHISPER_MODEL", "small")
        device = "cuda" if _cuda_available else "cpu"
        compute_type = "float16" if _cuda_available else "int8"
        _faster_model = WhisperModel(model_name, device=device, compute_type=compute_type)
    return _faster_model


def _load_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        import whisper
        model_name = os.environ.get("WHISPER_MODEL", "base")
        device = "cuda" if _cuda_available else "cpu"
        _whisper_model = whisper.load_model(model_name, device=device)
    return _whisper_model

def split_audio_in_memory(audio: AudioSegment, chunk_length_ms=120000):
    chunks = []
    for start in range(0, len(audio), chunk_length_ms):
        chunk = audio[start:start + chunk_length_ms]
        chunks.append(chunk)
    return chunks


def _transcribe_with_faster(audio_np: np.ndarray) -> str:
    model = _load_faster_model()
    segments, info = model.transcribe(audio_np, language="en")
    return " ".join([seg.text for seg in segments])


def _transcribe_with_whisper(audio_np: np.ndarray) -> str:
    model = _load_whisper_model()
    # whisper library expects either a file or a numpy array; it returns dict with 'text'
    result = model.transcribe(audio_np, language="en", task="transcribe")
    return result.get("text", "")


def transcribe_audio_bytes(audio_bytes: bytes) -> str:
    audio = convert_to_wav_16k_mono(audio_bytes)
    chunks = split_audio_in_memory(audio)
    transcript = []

    backend = os.environ.get("TRANSCRIBER_BACKEND", "auto")

    use_faster = False
    if backend == "faster-whisper":
        use_faster = _faster_available
    elif backend == "whisper":
        use_faster = False
    else:  # auto
        use_faster = _faster_available and _cuda_available

    for i, chunk in enumerate(chunks):
        audio_np = audiosegment_to_np(chunk)
        if use_faster:
            text = _transcribe_with_faster(audio_np)
        else:
            backend_choice = os.environ.get("TRANSCRIBER_BACKEND", "auto")
            if backend_choice in ("whisper-cpp", "whisper.cpp") or os.environ.get("TRANSCRIBER_BACKEND") == "whisper-cpp":
                text = _transcribe_with_whispercpp(chunk)
            else:
                text = _transcribe_with_whisper(audio_np)
        transcript.append(text)

    return " ".join(transcript)


def _transcribe_with_whispercpp(audio_segment: AudioSegment) -> str:
    """Transcribe using a local whisper.cpp (ggml) binary.

    Requires environment variables:
      - WHISPER_CPP_BIN: path to whisper.cpp main executable (or 'main' available on PATH)
      - WHISPER_CPP_MODEL: path to ggml model file (e.g., ggml-small.bin)

    This function writes the provided AudioSegment to a temporary WAV file and calls the binary.
    """
    import subprocess
    import tempfile
    from pathlib import Path

    whisper_bin = os.environ.get("WHISPER_CPP_BIN", "main")
    model_path = os.environ.get("WHISPER_CPP_MODEL")
    if not model_path:
        raise RuntimeError("WHISPER_CPP_MODEL environment variable must be set to the ggml model path")

    # Export audio_segment to a temporary wav file
    with tempfile.TemporaryDirectory() as td:
        audio_path = Path(td) / "input.wav"
        # Use pydub export; ensure PCM 16-bit WAV
        audio_segment.export(str(audio_path), format="wav", parameters=["-ac", "1", "-ar", "16000"])

        # Build command: whisper.cpp typically prints transcript to stdout
        cmd = [whisper_bin, "-m", model_path, "-f", str(audio_path), "-otxt"]
        # Allow overriding threads
        threads = os.environ.get("WHISPER_CPP_THREADS")
        if threads:
            cmd.extend(["-t", threads])

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=600)
            out = res.stdout.strip()
            # whisper.cpp tends to output the transcript lines; return as single string
            return out
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"whisper.cpp failed: {e.stderr or e.stdout}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("whisper.cpp timed out")

def clean_text(text: str) -> str:
    text = re.sub(r'\b(\w+)( \1\b)+', r'\1', text.strip())
    sentences = re.split(r'(?<=[.!?])\s+|\n+', text)
    cleaned = []

    for s in sentences:
        s = s.strip()
        if not s:
            continue
        s = s[0].upper() + s[1:] if len(s) > 1 else s.upper()
        if s[-1] not in ".!?":
            s += "."
        cleaned.append(s)

    return " ".join(cleaned)

def capitalize_entities(text: str, chunk_size=10000) -> str:
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    new_text = ""

    for chunk in chunks:
        nlp = _get_nlp()
        doc = nlp(chunk)
        offset = 0
        chunk_text = chunk
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG", "GPE", "LOC", "PRODUCT"]:
                start = ent.start_char + offset
                end = ent.end_char + offset
                chunk_text = chunk_text[:start] + ent.text.title() + chunk_text[end:]
                offset += len(ent.text.title()) - len(ent.text)
        new_text += chunk_text + " "

    return new_text.strip()

def format_paragraphs(text: str, max_sentences_per_para=5) -> str:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    paragraphs = [" ".join(sentences[i:i+max_sentences_per_para])
                  for i in range(0, len(sentences), max_sentences_per_para)]
    return "\n\n".join(paragraphs)

def process_audio_pipeline(audio_bytes: bytes) -> tuple[str, str]:
    raw_text = transcribe_audio_bytes(audio_bytes)
    polished_text = clean_text(raw_text)
    polished_text = capitalize_entities(polished_text)
    polished_text = format_paragraphs(polished_text)
    return raw_text, polished_text

# -------------------
# Example Local Test
# -------------------
if __name__ == "__main__":
    path = r"C:\Users\patry\Desktop\NexSum\test_data\test.mp3"
    with open(path, "rb") as f:
        audio_bytes = f.read()

    print("Processing audio...")
    raw, proper = process_audio_pipeline(audio_bytes)

    print("\n=== RAW TRANSCRIPT ===\n")
    print(raw)

    print("\n=== PROPER TRANSCRIPT ===\n")
    print(proper)
