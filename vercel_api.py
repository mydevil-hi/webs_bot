import os
import requests

VERCEL_TOKEN = os.environ.get("VERCEL_TOKEN")

def deploy_website_to_vercel(project_name: str, html_content: str):
    """
    يقوم برفع ملفات الموقع مباشرة إلى Vercel عبر الـ API ويعيد الرابط الناتج.
    """
    if not VERCEL_TOKEN:
        print("❌ تنبيه: مفتاح VERCEL_TOKEN غير موجود.")
        return None

    url = "https://api.vercel.com/v13/deployments"
    
    headers = {
        "Authorization": f"Bearer {VERCEL_TOKEN}",
        "Content-Type": "application/json"
    }

    files_payload = [
        {
            "file": "index.html",
            "data": html_content
        }
    ]

    payload = {
        "name": project_name.lower().replace(" ", "-")[:30],
        "files": files_payload,
        "projectSettings": {
            "framework": None
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        res_data = response.json()

        if response.status_code in [200, 201]:
            deployment_url = f"https://{res_data.get('url')}"
            return deployment_url
        else:
            print(f"⚠️ خطأ في الرفع إلى Vercel: {res_data}")
            return None
            
    except Exception as e:
        print(f"❌ خطأ في الاتصال بـ Vercel: {e}")
        return None
        
