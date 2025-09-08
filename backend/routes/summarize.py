from flask import request, jsonify
from . import api_bp
from backend.services.summarization_service import summarize_text

from flask import Blueprint, request, jsonify
from src.main import SummarizerApp

summarizer = SummarizerApp()

@api_bp.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"success": False, "error": "No text provided"}), 400

        text = data["text"]
        content_type = data.get("type")  # optional: academic/book/general/meeting TO DO!!!

        result = summarizer.summarize_text(text, content_type)
        return jsonify({"success": True, "data": result})

    except Exception as e:
        print(f"[ERROR] Summarization failed: {e}", flush=True)
        return jsonify({"success": False, "error": str(e)}), 500

