import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "data" / "flowpilot.db"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = "gemini-3.6-flash"