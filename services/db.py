import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bot_data.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Stats table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS downloads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            platform TEXT,
            downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id: int, username: str, full_name: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO users (user_id, username, full_name)
        VALUES (?, ?, ?)
    """, (user_id, username, full_name))
    conn.commit()
    conn.close()

def log_download(user_id: int, url: str):
    platform = "unknown"
    if "instagram.com" in url: platform = "instagram"
    elif "tiktok.com" in url: platform = "tiktok"
    elif "youtube.com" in url or "youtu.be" in url: platform = "youtube"
    elif "pinterest.com" in url or "pin.it" in url: platform = "pinterest"
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO downloads (user_id, platform)
        VALUES (?, ?)
    """, (user_id, platform))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM downloads")
    total_downloads = cursor.fetchone()[0]
    
    cursor.execute("SELECT platform, COUNT(*) FROM downloads GROUP BY platform")
    platform_stats = cursor.fetchall()
    
    conn.close()
    
    return {
        "total_users": total_users,
        "total_downloads": total_downloads,
        "platform_stats": platform_stats
    }
