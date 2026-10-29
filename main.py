import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from gemini_ai import generate_website_code
# سنقوم لاحقاً بربط الدوال الخاصة بـ Vercel و Supabase هنا

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
def cmd_start(message: types.Message):
    message.answer(
        "أهلاً بك! أنا بوت توليد ونشر المواقع بالذكاء الاصطناعي.\n\n"
        "أرسل لي فكرة موقعك وسأقوم ببنائه ورفعه لك فوراً!\n"
        "الأوامر المتاحة:\n"
        "/newweb - لبدء تصميم موقع جديد\n"
        "/myweb - لعرض مواقعي وإدارتها"
    )

@dp.message(Command("newweb"))
def cmd_newweb(message: types.Message):
    message.answer("ممتاز! اكتب لي الآن مواصفات وفكرة الموقع الذي ترغب في إنشائه بالتفصيل.")

# استقبال وصف الموقع وتوليده
@dp.message(F.text & ~F.text.startswith('/'))
async def handle_website_prompt(message: types.Message):
    await message.answer("⏳ جاري توليد وتصميم الموقع عبر الذكاء الاصطناعي، انتظر قليلاً...")
    
    # 1. توليد الكود عبر جيمناي
    html_code = generate_website_code(message.text)
    
    # (لاحقاً سنقوم برفع هذا الكود تلقائياً لـ Vercel هنا)
    
    await message.answer("✅ تم توليد الكود بنجاح!\n(جارٍ تطوير خطوة الرفع التلقائي لـ Vercel في الخطوة القادمة)...")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
  
