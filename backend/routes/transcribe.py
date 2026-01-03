from flask import request, jsonify
from werkzeug.utils import secure_filename
from . import api_bp
from backend.services.transcription_service import transcribe_audio_bytes
import logging

logger = logging.getLogger(__name__)

@api_bp.route("/transcribe", methods=["POST"])
def transcribe():
    try:
        if "audio" not in request.files:
            return jsonify({"success": False, "error": "No audio file uploaded"}), 400

        file = request.files["audio"]
        filename = secure_filename(file.filename or "")
        ext = f".{filename.rsplit('.', 1)[-1].lower()}" if "." in filename else ""
        logger.debug(f"Uploaded filename: {filename}")
        logger.debug(f"Detected extension: {ext}")

        ALLOWED_EXTS = {".mp3", ".wav", ".m4a"}
        if ext not in ALLOWED_EXTS:
            return jsonify({"success": False, "error": f"Unsupported file extension {ext}"}), 415

        audio_bytes = file.read()

        try:
            raw_text, polished_text = transcribe_audio_bytes(audio_bytes)
        except Exception as e:
            logger.exception("Transcription failed")
            return jsonify({"success": False, "error": str(e)}), 500

        return jsonify({
            "success": True,
            "data": {
                "raw_transcript": raw_text,
                "polished_transcript": polished_text
            }
        })

    except Exception as e:
        logger.exception("Unexpected server error")
        return jsonify({"success": False, "error": str(e)}), 500

