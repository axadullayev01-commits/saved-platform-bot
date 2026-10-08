import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ADMIN_ID = os.getenv("ADMIN_ID") # Admin user ID for the dashboard

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in .env")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in .env")
