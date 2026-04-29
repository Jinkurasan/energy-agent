import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def _get(key: str, default: str = "") -> str:
    try:
        import streamlit as st
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)

ANTHROPIC_API_KEY = _get("ANTHROPIC_API_KEY")
NOTION_API_KEY = _get("NOTION_API_KEY")
NOTION_DATABASE_ID = _get("NOTION_DATABASE_ID")
NOTE_EMAIL = _get("NOTE_EMAIL")
NOTE_PASSWORD = _get("NOTE_PASSWORD")
NIKKEI_EMAIL = _get("NIKKEI_EMAIL")
NIKKEI_PASSWORD = _get("NIKKEI_PASSWORD")

BASE_DIR = Path(__file__).parent
SESSION_DIR = BASE_DIR / "sessions"
SESSION_DIR.mkdir(exist_ok=True)

MODEL_HEAVY = "claude-opus-4-7"
MODEL_LIGHT = "claude-sonnet-4-6"
