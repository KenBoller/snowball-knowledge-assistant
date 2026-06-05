import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

APP_NAME = "Snowball Knowledge Assistant"
APP_VERSION = "0.1.0"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

UPLOAD_DIR = BASE_DIR / "uploads"
CHROMA_DIR = BASE_DIR / "chroma_store"