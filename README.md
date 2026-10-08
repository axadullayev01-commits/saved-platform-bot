# Saved Platform Bot

Bu loyiha turli platformalardan (Instagram, TikTok, YouTube Shorts, Pinterest) media fayllarni yuklab beruvchi va AI yordamida izohlar yozuvchi Telegram botidir.

## Asosiy Imkoniyatlar (Features)
- **Media Yuklab Olish**: `yt-dlp` orqali berilgan havoladan video yoki rasmlarni yuklab olish imkoniyati.
- **AI Izohlar (Captions)**: Google Gemini AI yordamida yuklab olingan media faylga moslashtirilgan, o'zbek tilida qisqacha izoh (caption) yaratish.
- **Audioni Ajratish**: Agar yuklab olingan fayl video bo'lsa, undan faqat audioni (mp3) ajratib olish va yuborish tugmasi (`inline button`).
- **Asl Izohni Ko'rish**: Medianing asl (original) izohini ko'rish imkoniyati.
- **Admin Panel**: Botning umumiy statistikasi (foydalanuvchilar va yuklanmalar soni)ni ko'rsatib turuvchi maxsus `/admin` bo'limi.
- **Dummy Server**: Render yoki shunga o'xshash cloud platformalarda 24/7 ishlashi uchun port ochib turuvchi oddiy HTTP server (bot.py ichida).

## Admin Panel va Sozlamalar (Admin Panel Setup)
- Botda admin panelga kirish uchun `/admin` komandasi ishlatiladi.
- Kimlar admin ekanligini belgilash uchun ularning Telegram ID raqami `.env` faylida (yoki Render'ning **Environment Variables** bo'limida) `ADMIN_ID` sifatida ko'rsatilishi kerak.
- **Bir nechta admin qo'shish**: Vergul orqali ajratib bir nechta adminni ham qo'shishingiz mumkin. Masalan: `ADMIN_ID=11111,22222,33333`
- **ID ni topish**: Agar foydalanuvchi admin bo'lmasa-yu `/admin` deb yozsa, bot avtomatik ravishda uning ID raqamini ko'rsatib, yordamchi xabar yozadi. Shu orqali o'z ID raqamingizni osongina topib olishingiz mumkin.
- **Render'ga Deploy**: Diqqat! `.env` fayli GitHub'ga yuklanmagani uchun (u `.gitignore`da yashiringan), Render'da botni ishga tushirishda `ADMIN_ID` kabi o'zgaruvchilarni bevosita Render'ning **Environment Variables** bo'limidan qo'lda kiritish kerak.

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
- `handlers/admin.py` - Admin panel mantiqlarini va statistikalarni chiqarish (`/admin` komandasi).
- `services/downloader.py` - `yt-dlp` orqali havoladan mediani yuklab olish funksiyalari.
- `services/gemini.py` - Google Gemini API ga ulanish va medianing nomiga qarab sun'iy intellekt yordamida caption yaratish.
- `services/db.py` - SQLite ma'lumotlar bazasi orqali foydalanuvchilar va yuklanmalar statistikasini yuritish.
- `utils/config.py` - Loyihadagi asosiy o'zgaruvchilarni (masalan, `BOT_TOKEN`) saqlaydi va yuklaydi.
- `Dockerfile` - Loyihani Docker konteyneriga o'rash uchun ko'rsatmalar.
- `requirements.txt` - Kerakli Python kutubxonalari ro'yxati.

## Kelajakdagi ishlar uchun yozuv (For AI Context)
*Ushbu fayl sun'iy intellekt (AI) yordamchisiga loyiha strukturasini tez tushunib olishi uchun maxsus yangilandi. Barcha muhim mantiqlar `services` va `handlers` papkalariga ajratilgan bo'lib, har qanday yangi funksiya (handler) kiritilganda `bot.py` dagi dispetcherga (dp) router sifatida qo'shilishi kerak.*