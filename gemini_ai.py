import google.generativeai as genai
import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

# قاموس لحفظ جلسات المحادثة لكل مستخدم لضمان بقاء الذاكرة والسياق أثناء الطلب
user_sessions = {}

def get_or_create_chat(user_id: int):
    """إنشاء أو جلب جلسة محادثة خاصة بكل مستخدم"""
    if user_id not in user_sessions:
        system_instruction = (
            "أنت مطور ويب خبير ومساعد ذكي. مهمتك هي مساعدة المستخدم في بناء مواقع وتطبيقات ويب كاملة. "
            "اكتب كود HTML متكامل (مع Tailwind CSS و JavaScript) بناءً على طلب المستخدم. "
            "عندما يطلب المستخدم إنشاء موقع، قم بتوليد الكود الصافي للموقع."
        )
        chat = model.start_chat(history=[])
        user_sessions[user_id] = chat
    return user_sessions[user_id]

def chat_with_ai(user_id: int, user_message: str) -> str:
    """إرسال رسالة المستخدم مع الحفاظ على سياق المحادثة السابقة"""
    chat = get_or_create_chat(user_id)
    response = chat.send_message(user_message)
    return response.text

def reset_user_chat(user_id: int):
    """إعادةsetting المحادثة لأمر /newweb"""
    if user_id in user_sessions:
        del user_sessions[user_id]
        
