# Saved Platform Bot

Bu loyiha turli platformalardan (Instagram, TikTok, YouTube Shorts, Pinterest) media fayllarni yuklab beruvchi va AI yordamida izohlar yozuvchi Telegram botidir.

## Asosiy Imkoniyatlar (Features)
- **Media Yuklab Olish**: `yt-dlp` orqali berilgan havoladan video yoki rasmlarni yuklab olish imkoniyati.
- **AI Izohlar (Captions)**: Google Gemini AI yordamida yuklab olingan media faylga moslashtirilgan, o'zbek tilida qisqacha izoh (caption) yaratish.
- **Audioni Ajratish**: Agar yuklab olingan fayl video bo'lsa, undan faqat audioni (mp3) ajratib olish va yuborish tugmasi (`inline button`).
- **Asl Izohni Ko'rish**: Medianing asl (original) izohini ko'rish imkoniyati.
- **Dummy Server**: Render yoki shunga o'xshash cloud platformalarda 24/7 ishlashi uchun port ochib turuvchi oddiy HTTP server (bot.py ichida).

## Texnologiyalar (Tech Stack)
- **Dasturlash tili**: Python 3
- **Kutubxonalar**: 
  - `aiogram` (v3.0+) - Telegram bot arxitekturasi uchun.
  - `yt-dlp` - turli xil platformalardan media ko'chirish uchun.
  - `google-genai` - Gemini orqali sun'iy intellekt xizmatlaridan foydalanish uchun.
  - `python-dotenv` - `.env` fayldan maxfiy kalitlarni o'qish uchun.

## Loyiha Strukturasi (Project Structure)
- `bot.py` - Loyihaning asosiy ishga tushish fayli. Aiogram routerlarini ulaydi va polling jarayonini boshlaydi.
- `handlers/media.py` - Botga kelgan xabarlarni va inline tugmalarni (callback_queries) qayta ishlash.
- `services/downloader.py` - `yt-dlp` orqali havoladan mediani yuklab olish funksiyalari.
- `services/gemini.py` - Google Gemini API ga ulanish va medianing nomiga qarab sun'iy intellekt yordamida caption yaratish.
- `utils/config.py` - Loyihadagi asosiy o'zgaruvchilarni (masalan, `BOT_TOKEN`) saqlaydi va yuklaydi.
- `Dockerfile` - Loyihani Docker konteyneriga o'rash uchun ko'rsatmalar.
- `requirements.txt` - Kerakli Python kutubxonalari ro'yxati.

## Kelajakdagi ishlar uchun yozuv (For AI Context)
*Ushbu fayl sun'iy intellekt (AI) yordamchisiga loyiha strukturasini tez tushunib olishi uchun maxsus yangilandi. Barcha muhim mantiqlar `services` va `handlers` papkalariga ajratilgan bo'lib, har qanday yangi funksiya (handler) kiritilganda `bot.py` dagi dispetcherga (dp) router sifatida qo'shilishi kerak.*