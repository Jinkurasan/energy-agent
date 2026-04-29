import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTE_EMAIL = os.getenv("NOTE_EMAIL")
NOTE_PASSWORD = os.getenv("NOTE_PASSWORD")
NIKKEI_EMAIL = os.getenv("NIKKEI_EMAIL")
NIKKEI_PASSWORD = os.getenv("NIKKEI_PASSWORD")

BASE_DIR = Path(__file__).parent
SESSION_DIR = BASE_DIR / "sessions"
SESSION_DIR.mkdir(exist_ok=True)

MODEL_HEAVY = "claude-opus-4-7"
MODEL_LIGHT = "claude-sonnet-4-6"
