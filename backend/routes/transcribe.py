from flask import request, jsonify
from werkzeug.utils import secure_filename
from . import api_bp
import backend.services.transcription_service as transcription_service
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

        ALLOWED_EXTS = {".mp3", ".wav", ".m4a", ".mp4"}
        if ext not in ALLOWED_EXTS:
            return jsonify({"success": False, "error": f"Unsupported file extension {ext}"}), 415

        audio_bytes = file.read()

        try:
            raw_text, polished_text = transcription_service.transcribe_audio_bytes(audio_bytes)
        except Exception as e:
            logger.exception("Transcription failed")
            return jsonify({"success": False, "error": str(e)}), 500

        try:
            from backend.services.content_service import detect_content_type
            detection = detect_content_type(polished_text)
        except Exception:
            detection = {"content_type": "general", "confidence": 0.0, "features": {}}

        return jsonify({
            "success": True,
            "data": {
                "raw_transcript": raw_text,
                "polished_transcript": polished_text,
                "content_type": detection.get("content_type"),
                "content_confidence": detection.get("confidence"),
                "content_features": detection.get("features"),
            }
        })

    except Exception as e:
        logger.exception("Unexpected server error")
        return jsonify({"success": False, "error": str(e)}), 500

