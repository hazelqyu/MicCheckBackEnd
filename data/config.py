# data/config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Set it in the .env file.")

OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o")
