import whisper
import re
import spacy
from pydub import AudioSegment
import io
import numpy as np

whisper_model = whisper.load_model("base")
nlp = spacy.load("en_core_web_sm")

def convert_to_wav_16k_mono(audio_bytes: bytes) -> AudioSegment:
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
    audio = audio.set_channels(1)       
    audio = audio.set_frame_rate(16000) 
    return audio

def audiosegment_to_np(audio: AudioSegment) -> np.ndarray:
    samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
    samples /= np.iinfo(audio.array_type).max
    return samples

def split_audio_in_memory(audio: AudioSegment, chunk_length_ms=120000):
    chunks = []
    for start in range(0, len(audio), chunk_length_ms):
        chunk = audio[start:start + chunk_length_ms]
        chunks.append(chunk)
    return chunks

def transcribe_audio_bytes(audio_bytes: bytes) -> str:
    audio = convert_to_wav_16k_mono(audio_bytes)
    chunks = split_audio_in_memory(audio)
    transcript = []

    for i, chunk in enumerate(chunks):
        print(f"Transcribing chunk {i+1}/{len(chunks)}...")
        audio_np = audiosegment_to_np(chunk)
        result = whisper_model.transcribe(audio_np, language="en", task="transcribe")
        transcript.append(result["text"])

    return " ".join(transcript)

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
