import os
import re
import uuid
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.downloader import download_media_async
from services.gemini import generate_caption_async

router = Router()

URL_PATTERN = re.compile(r'https?://[^\s]+')

# Cache URLs using short IDs to prevent BUTTON_DATA_INVALID (Telegram callback_data 64 byte limit)
MEDIA_CACHE = {}

@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer("Salom! Menga Instagram, TikTok, YouTube (Shorts), Pinterest yoki boshqa platformadan link yuboring, men uni yuklab beraman.")

@router.message(F.text.regexp(URL_PATTERN))
async def handle_url(message: Message):
    url = URL_PATTERN.search(message.text).group(0)
    processing_msg = await message.reply("⏳ Link tekshirilmoqda, kuting...")
    
    file_path = None
    try:
        media_info = await download_media_async(url)
        file_path = media_info["file_path"]
        title = media_info.get("title", "")
        desc = media_info.get("description", "")
        
        caption = await generate_caption_async(title, desc)
        
        media_file = FSInputFile(file_path)
        
        if media_info["type"] == "photo":
            await message.answer_photo(photo=media_file, caption=caption)
        else:
            # Generate a short ID for the callback data
            short_id = str(uuid.uuid4())[:8]
            MEDIA_CACHE[short_id] = url
            
            builder = InlineKeyboardBuilder()
            builder.button(text="🎵 Musiqasini yuklab olish", callback_data=f"audio|{short_id}")
            await message.answer_video(video=media_file, caption=caption, reply_markup=builder.as_markup())
            
    except Exception as e:
        await message.reply(f"❌ Xatolik yuz berdi: {str(e)}\n\nIltimos, link to'g'riligiga ishonch hosil qiling yoki keyinroq urinib ko'ring.")
    finally:
        await processing_msg.delete()
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

@router.callback_query(F.data.startswith("audio|"))
async def handle_audio_extraction(callback: CallbackQuery):
    short_id = callback.data.split("|", 1)[1]
    url = MEDIA_CACHE.get(short_id)
    
    if not url:
        await callback.answer("❌ Kechirasiz, bu havola muddati o'tgan yoki topilmadi.", show_alert=True)
        return
        
    await callback.message.answer("⏳ Audio ajratib olinmoqda...")
    await callback.answer()
    
    file_path = None
    try:
        media_info = await download_media_async(url, extract_audio=True)
        file_path = media_info["file_path"]
        
        audio_file = FSInputFile(file_path)
        await callback.message.answer_audio(audio=audio_file, caption="🎵 Audio ajratildi.")
    except Exception as e:
        await callback.message.answer(f"❌ Audioni ajratishda xatolik: {str(e)}")
    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
