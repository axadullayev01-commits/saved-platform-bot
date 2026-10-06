import asyncio
import logging
import threading
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from utils.config import BOT_TOKEN
from handlers.media import router as media_router

# Setup logging
logging.basicConfig(level=logging.INFO)

class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), DummyHandler)
    server.serve_forever()

async def main():
    # Start dummy web server for Render health check
    threading.Thread(target=run_dummy_server, daemon=True).start()
    
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    
    # Include routers
    dp.include_router(media_router)
    
    # Start polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
