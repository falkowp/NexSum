from flask import request, jsonify
from . import api_bp
import backend.services.summarization_service as summarization_service
import logging

logger = logging.getLogger(__name__)

@api_bp.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"success": False, "error": "No text provided"}), 400

        text = data["text"]
        content_type = data.get("type")  # optional: academic/book/general/meeting

        result = summarization_service.summarize_text(text, content_type)
        return jsonify({"success": True, "data": result})

    except Exception as e:
        logger.exception("Summarization failed")
        return jsonify({"success": False, "error": str(e)}), 500

