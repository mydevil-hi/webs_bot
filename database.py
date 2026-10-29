import os
from supabase import create_client, Client

# ضع مفاتيح Supabase الخاصة بك هنا أو في ملف Environment Variables
SUPABASE_URL = "YOUR_SUPABASE_URL"
SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_user_project(user_id: int, project_name: string, project_url: string):
    """حفظ بيانات الموقع الجديد للمستخدم في قاعدة البيانات"""
    data = {
        "user_id": user_id,
        "project_name": project_name,
        "project_url": project_url
    }
    response = supabase.table("user_projects").insert(data).execute()
    return response

def get_user_projects(user_id: int):
    """جلب قائمة كل مواقع المستخدم"""
    response = supabase.table("user_projects").select("*").eq("user_id", user_id).execute()
    return response.data

def delete_project_db(project_id: int):
    """حذف مشروع من القاعدة"""
    supabase.table("user_projects").delete().eq("id", project_id).execute()
  
