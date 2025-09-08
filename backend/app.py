import os
import sys
from pathlib import Path

from flask import Flask, jsonify
from flask_cors import CORS

# Ensure project root is on sys.path so we can import your existing src/ and config/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

def create_app():
    app = Flask(__name__)
    # Allow your React dev server (5173 = Vite, 3000 = CRA)
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://localhost:3000"]}})

    # Register API blueprints
    from backend.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/health")
    def health():
        return jsonify({"ok": True, "service": "NexSum API"})

    return app

app = create_app()

if __name__ == "__main__":
    # For local dev only; use gunicorn in prod/serverless adapters later
    app.run(host="127.0.0.1", port=5000, debug=True)
