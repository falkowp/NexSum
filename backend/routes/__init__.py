from flask import Blueprint

api_bp = Blueprint("api", __name__)

# Import routes so they get registered on the blueprint
from . import transcribe  # noqa: E402,F401
from . import summarize  # noqa: E402,F401
