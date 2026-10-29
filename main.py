import os
import asyncio
import logging
import threading
from fastapi import FastAPI, HTMLResponse
import uvicorn
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

from gemini_ai import chat_with_ai, reset_user_chat
from database import save_project_to_db, get_user_projects_from_db, delete_project_from_db
from vercel_api import deploy_website_to_vercel

# إعدادات البوت والتوكنات
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return "<h3>🚀 Webs Generator Bot is Running 24/7!</h3>"

# أمر البدء
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.InlineKeyboardButton(text="📂 مواقعي", callback_data="my_projects")],
        [types.InlineKeyboardButton(text="🆕 مشروع جديد (/newweb)", callback_data="new_web")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer(
        "مرحباً بك في بوت توليد ورفع المواقع بالذكاء الاصطناعي! 🚀\n"
        "اطلب مني تصميم أي موقع وسأقوم ببنائه ورفعه تلقائياً على Vercel.",
        reply_markup=keyboard
    )

# أمر موقع جديد
@dp.message(Command("newweb"))
async def cmd_newweb(message: types.Message):
    reset_user_chat(message.from_user.id)
    await message.answer("✨ تم بدء مشروع جديد! اطلب المواصفات التي تريدها للموقع.")

@dp.callback_query(lambda c: c.data == "new_web")
async def cb_newweb(callback: types.CallbackQuery):
    reset_user_chat(callback.from_user.id)
    await callback.message.answer("✨ تم بدء مشروع جديد! اكتب لي فكرة ومواصفات الموقع.")
    await callback.answer()

# زر مواقعي
@dp.callback_query(lambda c: c.data == "my_projects")
async def cb_my_projects(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    projects = get_user_projects_from_db(user_id)
    
    if not projects:
        await callback.message.answer("ليس لديك أي مواقع مرفوعة حتى الآن.")
        await callback.answer()
        return

    for p in projects:
        kb = [[types.InlineKeyboardButton(text="🗑️ حذف الموقع", callback_data=f"del_{p['id']}")]]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
        await callback.message.answer(
            f"🌐 **{p['project_name']}**\n🔗 {p['project_url']}",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    await callback.answer()

# حذف مشروع
@dp.callback_query(lambda c: c.data.startswith("del_"))
async def cb_delete(callback: types.CallbackQuery):
    project_id = int(callback.data.split("_")[1])
    if delete_project_from_db(project_id):
        await callback.message.edit_text("✅ تم حذف الموقع بنجاح.")
    else:
        await callback.message.edit_text("❌ حدث خطأ أثناء الحذف.")
    await callback.answer()

# استقبال طلبات تصميم المواقع والتعامل مع الذكاء الاصطناعي
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    user_text = message.text

    await message.answer("⏳ جاري توليد وتصميم الموقع عبر الذكاء الاصطناعي...")
    
    # استدعاء جيمناي لتوليد الكود
    ai_response = chat_with_ai(user_id, user_text)
    
    # استخراج كود HTML من رد الذكاء الاصطناعي (افتراض أنه محاط بوسم كود أو كامل النص)
    html_code = ai_response
    if "```html" in ai_response:
        html_code = ai_response.split("```html")[1].split("```")[0].strip()
    elif "```" in ai_response:
        html_code = ai_response.split("```")[1].split("```")[0].strip()

    await message.answer("🚀 جاري رفع الموقع تلقائياً على Vercel...")
    
    # اسم افتراضي للمشروع مستمد من أول كلمات طلب المستخدم
    project_name = f"web-{user_id}-{abs(hash(user_text)) % 1000}"
    
    # رفع الملف لـ Vercel
    deploy_url = deploy_website_to_vercel(project_name, html_code)
    
    if deploy_url:
        # حفظ الرابط في قاعدة البيانات
        save_project_to_db(user_id, project_name, deploy_url)
        await message.answer(
            f"🎉 **تم نشر موقعك بنجاح!**\n\n🔗 الرابط: {deploy_url}",
            parse_mode="Markdown"
        )
    else:
        await message.answer("⚠️ حدث خطأ أثناء عملية الرفع على Vercel، حاول مرة أخرى.")

# تشغيل سيرفر الويب في الخلفية ليظل البوت نشطاً 24/7 على منصات الاستضافة
def run_web():
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

async def main():
    # تشغيل السيرفر بالتزامن مع البوت
    server_thread = threading.Thread(target=run_web, daemon=True)
    server_thread.start()
    
    print("Bot is starting polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
