FROM python:3.11-slim

# yt-dlp video/audio fayllarni ishlashi uchun ffmpeg kerak bo'ladi
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Kutubxonalarni o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Barcha fayllarni ko'chirish
COPY . .

# Botni ishga tushirish
CMD ["python", "bot.py"]
