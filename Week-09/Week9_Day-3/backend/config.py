import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "").strip() or "gemini-2.5-flash"
BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1").strip()
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000").strip()


def validate_config() -> None:
    """Validates that required configuration is present."""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY is not set or contains a placeholder value in the environment / .env file.")
