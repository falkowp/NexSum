import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_SETTINGS = {
    "summary_length": 5,
    "keyphrase_count": 10,
    "chunk_size": 1000,
    "model_name": "facebook/bart-large-cnn"
}

FILE_SETTINGS = {
    "allowed_extensions": [".txt", ".pdf", ".docx"],
    "max_file_size": 10 * 1024 * 1024
}

PROCESSING_SETTINGS = {
    "min_text_length": 50,
    "max_summary_length": 150,
    "min_summary_length": 20
}