from flask import request, jsonify
from . import api_bp
from backend.services.summarization_service import summarize_text

@api_bp.post("/summarize")
def summarize():
    payload = request.get_json(silent=True) or {}
    text = payload.get("text", "")
    content_type = payload.get("type")  # 'academic', 'book', 'general', 'meeting', or None

    if not text or not isinstance(text, str):
        return jsonify({"success": False, "error": "Field 'text' (string) is required"}), 400

    try:
        result = summarize_text(text, content_type)
        # result is already a dict from your SummarizerApp.summarize_text
        return jsonify(result), (200 if result.get("success") else 400)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
