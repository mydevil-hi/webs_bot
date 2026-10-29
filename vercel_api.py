import requests
import os

# جلب توكن Vercel من متغيرات البيئة (Environment Variables) التي ضبطتها في Render
VERCEL_TOKEN = os.environ.get("VERCEL_TOKEN")

def deploy_to_vercel(project_name: str, html_content: str):
    """
    تقوم هذه الدالة بإنشاء ونشر موقع ثابت (Static Website) على Vercel مباشرة
    عبر الـ API الخاص بهم.
    """
    url = "https://api.vercel.com/v13/deployments"
    
    headers = {
        "Authorization": f"Bearer {VERCEL_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # تنظيف اسم المشروع (Vercel يرفض الأحرف الكبيرة والمسافات في أسماء المشاريع)
    clean_project_name = project_name.lower().replace("_", "-").replace(" ", "-")
    
    # تجهيز بنية الملفات (نرفع ملف index.html يحتوي على كود الموقع)
    payload = {
        "name": clean_project_name,
        "files": [
            {
                "file": "index.html",
                "data": html_content
            }
        ],
        "projectSettings": {
            "framework": None # موقع HTML ثابت عادي بدون أطر عمل معقدة
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        # Vercel يعيد 200 أو 201 عند نجاح عملية النشر
        if response.status_code in [200, 201]:
            data = response.json()
            # استخراج رابط الموقع الشغال من الرد
            site_url = data.get("url")
            
            # أحياناً يعود الرابط بدون https:// في بدايته، فنضيفه للتأكد
            if not site_url.startswith("http"):
                site_url = f"https://{site_url}"
                
            return {
                "success": True,
                "url": site_url
            }
        else:
            # في حال حدث خطأ من جهة Vercel (مثل اسم مشروع محجوز أو توكن خطأ)
            return {
                "success": False,
                "error": response.text
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
      
