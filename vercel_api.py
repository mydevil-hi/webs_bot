import os
import requests

VERCEL_TOKEN = os.environ.get("VERCEL_TOKEN")
# يمكنك ربط مشروع واحد رئيسي على Vercel ليعمل كـ Wildcard، أو استخدام معرف الفريق إن وجد
VERCEL_PROJECT_NAME = os.environ.get("VERCEL_PROJECT_NAME", "my-ai-web-deployer")

def deploy_website_to_vercel(project_name: str, html_content: str, css_content: str = "", js_content: str = ""):
    """
    يقوم برفع ملفات الموقع (HTML, CSS, JS) مباشرة إلى Vercel عبر الـ API
    ويعيد رابط الموقع الناتج.
    """
    if not VERCEL_TOKEN:
        print("❌ تنبيه: مفتاح VERCEL_TOKEN غير موجود في المتغيرات البيئية.")
        return None

    url = "https://api.vercel.com/v13/deployments"
    
    headers = {
        "Authorization": f"Bearer {VERCEL_TOKEN}",
        "Content-Type": "application/json"
    }

    # تجهيز الملفات التي سيتم نشرها
    files_payload = [
        {
            "file": "index.html",
            "data": html_content
        }
    ]
    
    if css_content:
        files_payload.append({
            "file": "style.css",
            "data": css_content
        })
        
    if js_content:
        files_payload.append({
            "file": "script.js",
            "data": js_content
        })

    payload = {
        "name": project_name.lower().replace(" ", "-"),
        "files": files_payload,
        "projectSettings": {
            "framework": None
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        res_data = response.json()

        if response.status_code in [200, 201]:
            # الحصول على الرابط الخاص بالنشر
            deployment_url = f"https://{res_data.get('url')}"
            return deployment_url
        else:
            print(f"⚠️ خطأ في الرفع إلى Vercel: {res_data}")
            return None
            
    except Exception as e:
        print(f"❌ حدث استثناء أثناء الاتصال بـ Vercel API: {e}")
        return None
