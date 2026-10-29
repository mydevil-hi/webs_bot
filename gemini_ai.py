import google.generativeai as genai
import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

# قاموس لحفظ جلسات المحادثة لكل مستخدم (حتى تبقى الذاكرة شغالة أثناء الطلب)
user_sessions = {}

def get_or_create_chat(user_id: int):
    """إنشاء أو جلب جلسة محادثة خاصة بكل مستخدم"""
    if user_id not in user_sessions:
        # نبدأ محادثة جديدة مع تعليمات النظام الثابتة
        system_instruction = (
            "أنت مطور ويب خبير ومساعد ذكي. مهمتك هي مساعدة المستخدم في بناء مواقع وتطبيقات ويب كاملة. "
            "اكتب كود HTML متكامل (مع Tailwind CSS و JavaScript) بناءً على طلب المستخدم. "
            "إذا احتجت إلى مفاتيح API خارجية (مثل Weather API أو غيرها)، اطلبها من المستخدم بوضوح في ردك أو اقترحها. "
            "عندما يكتمل الكود أو يطلب المستخدم تصديره، اكتب الكود الصافي بداخل وسم كود مناسب."
        )
        # نستخدم chat session لضمان تواصل الأفكار والذاكرة
        chat = model.start_chat(history=[])
        user_sessions[user_id] = chat
    return user_sessions[user_id]

def chat_with_ai(user_id: int, user_message: str) -> str:
    """إرسال رسالة المستخدم مع الحفاظ على سياق المحادثة السابقة"""
    chat = get_or_create_chat(user_id)
    response = chat.send_message(user_message)
    return response.text
