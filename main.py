import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from gemini_ai import chat_with_ai
from vercel_api import deploy_to_vercel
from database import save_project_to_db, get_user_projects_from_db, delete_project_from_db

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "أهلاً بيك يا غالي! 🤖\n"
        "أنا بوت تطوير وتصميم المواقع بالذكاء الاصطناعي ورفعها فوراً على Vercel.\n\n"
        "الأوامر المتاحة:\n"
        "🔹 /newweb - لبدء فكرة وموقع جديد\n"
        "🔹 /myweb - لعرض كل مواقعك السابقة وإدارتها\n"
    )

@dp.message(Command("newweb"))
async def cmd_newweb(message: types.Message):
    await message.answer("💡 ممتاز! سولف لي شنو فكرة الموقع اللي تريد تسويه؟ (مثلاً: موقع بورتفوليو، صفحة هبوط لمنتج، موقع طقس...)")

# أمر عرض المواقع المحفوظة
@dp.message(Command("myweb"))
async def cmd_myweb(message: types.Message):
    user_id = message.from_user.id
    projects = get_user_projects_from_db(user_id)
    
    if not projects:
        await message.answer("📂 ليس لديك أي مواقع مسجلة حتى الآن. استخدم /newweb لإنشاء أول موقع!")
        return
    
    await message.answer("📂 هذه قائمة مواقعك التي أنشأتها:")
    for proj in projects:
        # إنشاء أزرار تفاعلية لكل موقع (رابط + زر حذف)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🌐 زيارة الموقع", url=proj['project_url']),
                InlineKeyboardButton(text="🗑️ حذف", callback_data=f"del_{proj['id']}")
            ]
        ])
        await message.answer(f"📌 **اسم المشروع:** `{proj['project_name']}`\n🔗 **الرابط:** {proj['project_url']}", reply_markup=keyboard)

# معالجة الضغط على زر الحذف
@dp.callback_query(F.data.startswith("del_"))
async def process_delete(callback: types.CallbackQuery):
    project_id = int(callback.data.split("_")[1])
    delete_project_from_db(project_id)
    await callback.message.edit_text("🗑️ تم حذف الموقع من القائمة بنجاح.")
    await callback.answer()

# استقبال رسائل المحادثة وإنشاء المواقع
@dp.message(F.text & ~F.text.startswith('/'))
async def handle_chat(message: types.Message):
    user_id = message.from_user.id
    
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    # 1. إرسال الرسالة لـ Gemini
    ai_response = chat_with_ai(user_id, message.text)
    
    # التحقق هل الرد يحتوي على كود HTML كامل لنشره
    if "<html>" in ai_response.lower() or "<!doctype html>" in ai_response.lower():
        await message.answer("⏳ تم توليد كود الموقع، جارٍ رفعه على Vercel تلقائياً...")
        
        project_name = f"web-{user_id}-{os.urandom(3).hex()}"
        
        # استخراج الكود (يمكنك تحسين الاستخراج لاحقاً إذا احتجت)
        html_code = ai_response
        
        # 2. الرفع على Vercel
        deploy_res = deploy_to_vercel(project_name, html_code)
        
        if deploy_res["success"]:
            site_url = deploy_res["url"]
            
            # 3. حفظ المشروع في قاعدة بيانات Supabase
            save_project_to_db(user_id, project_name, site_url)
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🌐 استعراض الموقع", url=site_url)]
            ])
            
            await message.answer(
                f"🎉 **تم نشر موقعك بنجاح!**\n\n"
                f"🔗 الرابط: {site_url}\n\n"
                f"تم حفظ الموقع في سجلك. يمكنك استعراض جميع مواقعك عبر أمر `/myweb`.",
                reply_markup=keyboard
            )
        else:
            await message.answer(f"❌ حدث خطأ أثناء الرفع لـ Vercel:\n{deploy_res['error']}")
    else:
        # إذا كان الذكاء الاصطناعي يسأل عن معلومات أو تفاصيل إضافية
        await message.answer(ai_response)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    
