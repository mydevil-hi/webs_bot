import os
from supabase import create_client, Client

# جلب بيانات الاتصال من متغيرات البيئة في Render
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_project_to_db(user_id: int, project_name: str, project_url: str):
    """حفظ تفاصيل الموقع الجديد في جدول user_projects"""
    try:
        data = {
            "user_id": user_id,
            "project_name": project_name,
            "project_url": project_url
        }
        response = supabase.table("user_projects").insert(data).execute()
        return True
    except Exception as e:
        print(f"Error saving to database: {e}")
        return False

def get_user_projects_from_db(user_id: int):
    """جلب كل المواقع الخاصة بالمستخدم من قاعدة البيانات"""
    try:
        response = supabase.table("user_projects").select("*").eq("user_id", user_id).execute()
        return response.data
    except Exception as e:
        print(f"Error fetching from database: {e}")
        return []

def delete_project_from_db(project_id: int):
    """حذف مشروع من القاعدة بناءً على الـ ID الخاص به"""
    try:
        supabase.table("user_projects").delete().eq("id", project_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting from database: {e}")
        return False
        
