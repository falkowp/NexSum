# NexSum

AI-powered audio transcription and intelligent text summarization system with content-type detection.

## Overview

NexSum is an end-to-end solution for converting audio recordings into structured, category-specific summaries. The system automatically transcribes audio using OpenAI Whisper, classifies content type (meeting, academic, book, or general), and generates tailored summaries using local LLM inference via Ollama.

## Key Features

- **Audio Transcription**: High-accuracy transcription using OpenAI Whisper
- **Content Classification**: Machine learning-based detection of content types using sentence embeddings
- **Category-Specific Summarization**: Customized summary templates for different content types
- **Local LLM Processing**: Privacy-focused summarization using Ollama (llama3.2:3b)
- **Structured Output**: Category-appropriate formatting (executive summaries, academic abstracts, etc.)
- **REST API**: Flask backend with CORS-enabled endpoints
- **Modern Web Interface**: React frontend with drag-and-drop audio upload

## Project Structure

```
NexSum/
├── backend/              # Flask API server
│   ├── app.py           # Application entry point
│   ├── routes/          # API endpoints (transcribe, summarize)
│   └── services/        # Business logic layer
├── src/                 # Core summarization engine
│   ├── core/            # Content detection and classification
│   ├── text_processing/ # Content-specific processors
│   ├── models/          # Extractors and summarizers
│   ├── config/          # Templates and settings
│   └── transcription/   # Whisper integration
├── frontend/            # React + Vite web application
├── tests/               # Pytest test suite
└── test_data/           # Sample texts for testing
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- ffmpeg (for audio processing)
- Ollama (for local LLM inference)

## Installation

### 1. Python Environment Setup

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Install System Dependencies

Install ffmpeg (required for audio processing):

```powershell
choco install ffmpeg
```

### 3. Download Language Models

Download the spaCy English model:

```powershell
python -m spacy download en_core_web_sm
```

Note: OpenAI Whisper will download its model (base) on first use.

### 4. Setup Ollama

Install Ollama from [ollama.ai](https://ollama.ai) and pull the required model:

```powershell
ollama pull llama3.2:3b
```

Ensure Ollama is running on `http://localhost:11434`.

### 5. Frontend Dependencies

```powershell
cd frontend
npm install
```

## Running the Application

### Start Backend Server

From the project root:

```powershell
python backend/app.py
```

Backend runs on `http://127.0.0.1:5000`

### Start Frontend Development Server

```powershell
cd frontend
npm run dev
```

Frontend runs on `http://localhost:5173`

Alternatively, run both servers simultaneously from the frontend directory:

```powershell
npm run dev-all
```

## Usage

### Web Interface

1. Navigate to `http://localhost:5173`
2. Upload an audio file (MP3, WAV, M4A, etc.)
3. Select content type or use automatic detection
4. View transcription and generated summary

### Command Line Interface

Process text directly using the CLI:

```powershell
python -m src.main --input text_file.txt --output summary.json
```

### API Endpoints

**Transcribe Audio**
```
POST /api/transcribe
Content-Type: multipart/form-data
Body: audio file
```

**Generate Summary**
```
POST /api/summarize
Content-Type: application/json
Body: {"text": "...", "content_type": "meeting"}
```

## Content Types

NexSum supports four content categories with specialized processing:

- **Meeting**: Executive summaries, decisions, action items
- **Academic**: Research questions, methodology, findings
- **Book**: Synopsis, themes, character analysis
- **General**: TL;DR, key points, recommendations

## Testing

Run the test suite:

```powershell
pytest
```

Run specific test categories:

```powershell
pytest tests/test_content_classifier.py -v
pytest tests/test_summarizer_llm_integration.py -v
```

## Configuration

Configuration files are located in `src/config/`:

- `settings.py`: Model paths and API settings
- `output_config.py`: Summary templates per content type
- `models.py`: Data models and type definitions

## Technology Stack

**Backend**
- Flask 3.0.3 with CORS support
- OpenAI Whisper for transcription
- Sentence Transformers for embeddings
- Scikit-learn for classification
- Ollama for LLM inference

**Frontend**
- React 18
- Vite build tool
- Modern ES6+ JavaScript

**NLP & ML**
- spaCy for text processing
- NLTK for linguistic analysis
- PyTorch for model inference
- Transformers library for fallback summarization

## Troubleshooting

**Audio Processing Errors**
- Ensure ffmpeg is installed and in PATH
- Verify audio file format is supported

**Transcription Issues**
- First run downloads Whisper model (may take several minutes)
- Check available disk space for model storage

**Summarization Failures**
- Verify Ollama is running: `ollama list`
- Check model is available: `ollama pull llama3.2:3b`
- System falls back to local transformers model if Ollama unavailable

**Import Errors**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` to install missing dependencies
- Download spaCy model: `python -m spacy download en_core_web_sm`

## License

This project is available for academic and research purposes.

## Contributing

Contributions are welcome. Please ensure all tests pass before submitting pull requests.
