from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from . import api_bp
from src.transcription.transcriber import process_audio_pipeline

@api_bp.route("/transcribe", methods=["POST"])
def transcribe():
    try:
        if "audio" not in request.files:
            return jsonify({"success": False, "error": "No audio file uploaded"}), 400

        file = request.files["audio"]
        filename = secure_filename(file.filename or "")
        ext = f".{filename.rsplit('.', 1)[-1].lower()}" if "." in filename else ""
        print(f"[DEBUG] Uploaded filename: {filename}")
        print(f"[DEBUG] Detected extension: {ext}")

        ALLOWED_EXTS = {".mp3", ".wav", ".m4a"}
        if ext not in ALLOWED_EXTS:
            return jsonify({"success": False, "error": f"Unsupported file extension {ext}"}), 415

        audio_bytes = file.read()

        # Process transcription pipeline with try/except
        try:
            raw_text, polished_text = process_audio_pipeline(audio_bytes)
        except Exception as e:
            print(f"[ERROR] Transcription failed: {e}", flush=True)
            return jsonify({"success": False, "error": str(e)}), 500

        return jsonify({
            "success": True,
            "data": {
                "raw_transcript": raw_text,
                "polished_transcript": polished_text
            }
        })

    except Exception as e:
        print(f"[ERROR] Unexpected server error: {e}", flush=True)
        return jsonify({"success": False, "error": str(e)}), 500

