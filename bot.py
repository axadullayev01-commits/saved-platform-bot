import asyncio
import logging
import threading
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from utils.config import BOT_TOKEN
from services.db import init_db, get_stats, get_all_users, get_recent_downloads
from handlers.media import router as media_router
from handlers.admin import router as admin_router

# Setup logging
logging.basicConfig(level=logging.INFO)

class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/admin-dashboard':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            stats = get_stats()
            users = get_all_users()
            downloads = get_recent_downloads(50)
            
            html = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Admin Dashboard</title>
                <script src="https://telegram.org/js/telegram-web-app.js"></script>
                <style>
                    body {{ font-family: sans-serif; padding: 15px; color: var(--tg-theme-text-color, #000); background-color: var(--tg-theme-bg-color, #fff); }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px; }}
                    th, td {{ border: 1px solid #ddd; padding: 6px; text-align: left; }}
                    th {{ background-color: var(--tg-theme-button-color, #3390ec); color: var(--tg-theme-button-text-color, #fff); }}
                    .card {{ border: 1px solid #ccc; padding: 10px; margin-bottom: 15px; border-radius: 8px; background-color: var(--tg-theme-secondary-bg-color, #f4f4f5); }}
                </style>
            </head>
            <body>
                <h2>📊 To'liq Statistika</h2>
                <div class="card">
                    <b>Jami foydalanuvchilar:</b> {stats['total_users']}<br>
                    <b>Jami yuklanmalar:</b> {stats['total_downloads']}
                </div>
                
                <h3>👥 So'nggi foydalanuvchilar</h3>
                <table>
                    <tr><th>Ism</th><th>Username</th></tr>
                    {"".join(f"<tr><td>{u[2]}</td><td>{u[1] or '-'}</td></tr>" for u in users[:50])}
                </table>

                <h3>⬇️ So'nggi yuklanmalar</h3>
                <table>
                    <tr><th>Platforma</th><th>Foydalanuvchi</th></tr>
                    {"".join(f"<tr><td>{d[0]}</td><td>{d[2] or d[3]}</td></tr>" for d in downloads[:50])}
                </table>
                <script>
                    window.Telegram.WebApp.ready();
                    window.Telegram.WebApp.expand();
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), DummyHandler)
    server.serve_forever()

async def main():
    # Initialize Database
    init_db()
    
    # Start dummy web server for Render health check
    threading.Thread(target=run_dummy_server, daemon=True).start()
    
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    
    # Include routers
    dp.include_router(admin_router)
    dp.include_router(media_router)
    
    # Start polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
