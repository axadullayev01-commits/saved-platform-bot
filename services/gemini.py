import os
from google import genai
from utils.config import GEMINI_API_KEY
import asyncio

# Initialize GenAI client
client = genai.Client(api_key=GEMINI_API_KEY)

def _generate_caption(title: str, description: str) -> str:
    prompt = f"Title: {title}\nDescription: {description}\nGenerate a creative, engaging 2-line Telegram caption with relevant emojis based on the title. Only output the caption."
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        # Fallback gracefully
        return title

async def generate_caption_async(title: str, description: str) -> str:
    """Generate caption using Gemini in a separate thread."""
    return await asyncio.to_thread(_generate_caption, title, description)
