import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SUBSCRIPTIONS_FILE = BASE_DIR / "subscriptions.json"
ANSWERS_FILE = BASE_DIR / "answers.json"
QUESTIONS_FILE = BASE_DIR / "questions.json"

# GPT
MAX_HISTORY_LEN = 10
GPT_MODEL = "gpt-4o-mini"
GPT_TEMP = 0.7
