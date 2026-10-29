import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from gemini_ai import chat_with_ai
from vercel_api import deploy_to_vercel
# استيراد دوال قاعدة البيانات إذا جهزتها بملف database.py

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "اهلاً بيك! 🤖\n"
        "أنا بوت تطوير وتصميم المواقع بالذكاء الاصطناعي.\n\n"
        "الأوامر المتاحة:\n"
        "🔹 /newweb - لبدء فكرة وموقع جديد\n"
        "🔹 /myweb - لعرض مواقعك السابقة وإدارتها\n\n"
        "اكتب /newweb ونخلينا نبدأ فكرتك الأولى!"
    )

@dp.message(Command("newweb"))
async def cmd_newweb(message: types.Message):
    await message.answer("💡 ممتاز! سولف لي شنو فكرة الموقع اللي تريد تسويه؟ (مثلاً: موقع بورتفوليو شخصي، متجر إلكتروني، صفحة طقس... إلخ)")

# استقبال ردود المستخدم ومحادثته بشكل مستمر
@dp.message(F.text & ~F.text.startswith('/'))
async def handle_chat(message: types.Message):
    user_id = message.from_user.id
    
    await message.action("typing") # إظهار حالة جاري الكتابة...
    
    # 1. إرسال الرسالة لـ Gemini مع الذاكرة المستمرة
    ai_response = chat_with_ai(user_id, message.text)
    
    # نتحقق إذا الذكاء الاصطناعي رد بكود HTML جاهز للنشر أو يريد مناقشة تفاصيل
    if "<html>" in ai_response.lower() or "<!doctype html>" in ai_response.lower():
        await message.answer("⏳ تم توليد كود الموقع، جارٍ رفعه على Vercel الآن...")
        
        # استخراج اسم مشروع عشوائي أو تنظيمي
        project_name = f"web-{user_id}-{os.urandom(3).hex()}"
        
        # استخراج الكود الصافي (يمكن تعديل طريقة الاستخراج حسب الحاجة)
        html_code = ai_response # يفضل استخراج ما بين علامات الـ code blocks إذا لزم
        
        # 2. الرفع التلقائي على Vercel
        deploy_res = deploy_to_vercel(project_name, html_code)
        
        if deploy_res["success"]:
            site_url = deploy_res["url"]
            await message.answer(
                f"🎉 **تم نشر موقعك بنجاح!**\n\n"
                f"🔗 الرابط: {site_url}\n\n"
                f"إذا تريد تعدل عليه شي أو تضيف ميزات، اكُتب لي التعديل وراح أحدثه لك فوراً!"
            )
            # هنا يمكنك إضافة كود حفظ الرابط في Supabase
        else:
            await message.answer(f"❌ حدث خطأ أثناء الرفع لـ Vercel:\n{deploy_res['error']}")
    else:
        # إذا كان الذكاء الاصطناعي يسأل عن تفاصيل أو يقترح API إضافي
        await message.answer(ai_response)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    
