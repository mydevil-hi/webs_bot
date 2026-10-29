import google.generativeai as genai

# ضع مفتاح Gemini API الخاص بك هنا
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=GEMINI_API_KEY)

# استخدام نموذج Gemini Flash السريع والمجاني
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_website_code(prompt_description: str) -> str:
    """يطلب من جيمناي تصميم موقع كامل بملف واحد HTML متضمن التنسيقات والجافاسكريبت"""
    system_instruction = (
        "أنت مطور وادوات ويب محترف. اكتب كود HTML كامل ومتكامل (يحتوي على Tailwind CSS عبر CDN و JavaScript داخلي إذا لزم الأمر) "
        "بناءً على طلب المستخدم. أجب فقط بكود الـ HTML الصافي بدون أي شرح إضافي، وبدون وسوم ماركداون إضافية غير الكود نفسه."
    )
    
    full_prompt = f"{system_instruction}\n\nطلب المستخدم للموقع: {prompt_description}"
    
    response = model.generate_content(full_prompt)
    return response.text
  
