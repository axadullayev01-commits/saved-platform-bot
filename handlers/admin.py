from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.config import ADMIN_ID
from services.db import get_stats

router = Router()

def is_admin(user_id):
    if not ADMIN_ID:
        return False
    # Ruxsat berilgan adminlar ro'yxatini vergul orqali ajratib tekshiramiz
    admin_ids = [i.strip() for i in str(ADMIN_ID).split(',')]
    return str(user_id) in admin_ids

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        await message.reply(f"Siz admin emassiz!\nSizning ID raqamingiz: <code>{message.from_user.id}</code>\nUshbu ID ni .env faylidagi ADMIN_ID ga qo'shing.", parse_mode="HTML")
        return
        
    stats = get_stats()
    
    text = f"📊 <b>Admin Dashboard</b>\n\n"
    text += f"👥 Umumiy foydalanuvchilar: <b>{stats['total_users']}</b>\n"
    text += f"⬇️ Umumiy yuklanmalar: <b>{stats['total_downloads']}</b>\n\n"
    
    if stats['platform_stats']:
        text += "📈 <b>Platformalar bo'yicha:</b>\n"
        for platform, count in stats['platform_stats']:
            text += f" - {platform.capitalize()}: <b>{count}</b>\n"
            
    builder = InlineKeyboardBuilder()
    builder.button(text="🔄 Yangilash", callback_data="admin_refresh")
    
    await message.answer(text, reply_markup=builder.as_markup())

@router.callback_query(F.data == "admin_refresh")
async def refresh_admin_panel(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Siz admin emassiz!", show_alert=True)
        return
        
    stats = get_stats()
    
    text = f"📊 <b>Admin Dashboard</b>\n\n"
    text += f"👥 Umumiy foydalanuvchilar: <b>{stats['total_users']}</b>\n"
    text += f"⬇️ Umumiy yuklanmalar: <b>{stats['total_downloads']}</b>\n\n"
    
    if stats['platform_stats']:
        text += "📈 <b>Platformalar bo'yicha:</b>\n"
        for platform, count in stats['platform_stats']:
            text += f" - {platform.capitalize()}: <b>{count}</b>\n"
            
    text += "\n<i>So'nggi yangilanish: hozir</i>"
            
    builder = InlineKeyboardBuilder()
    builder.button(text="🔄 Yangilash", callback_data="admin_refresh")
    
    try:
        await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    except Exception:
        pass # Message content might not have changed
        
    await callback.answer("Yangilandi!")
