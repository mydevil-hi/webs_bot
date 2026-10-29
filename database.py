import os
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def init_database():
    """
    محاولة إنشاء الجدول تلقائياً عبر SQL إذا لم يكن موجوداً،
    لتجنب الأخطاء وضمان توافق تام مع البوت.
    """
    sql_query = """
    CREATE TABLE IF NOT EXISTS user_projects (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        project_name TEXT NOT NULL,
        project_url TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """
    try:
        # تنفيذ الاستعلام عبر ميزة الـ RPC أو الـ PostgREST
        # ملاحظة: Supabase قد تتطلب تفعيل صلاحية تنفيذ الـ SQL، 
        # لذا إذا أعطى تنبيه، فالإنشاء اليدوي لمرة واحدة يظل الخيار البديل الأضمن.
        supabase.postgrest.session.post(
            f"{SUPABASE_URL}/rest/v1/rpc/exec_sql",
            headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"},
            json={"query": sql_query}
        )
        print("✅ تم التحقق من قاعدة البيانات والجدول بنجاح.")
    except Exception as e:
        print(f"⚠️ ملاحظة حول الإنشاء التلقائي (تأكد من إنشاء الجدول يدوياً إذا ظهر خطأ): {e}")

def save_project_to_db(user_id: int, project_name: str, project_url: str):
    try:
        data = {
            "user_id": user_id,
            "project_name": project_name,
            "project_url": project_url
        }
        supabase.table("user_projects").insert(data).execute()
        return True
    except Exception as e:
        print(f"Error saving to database: {e}")
        return False

def get_user_projects_from_db(user_id: int):
    try:
        response = supabase.table("user_projects").select("*").eq("user_id", user_id).execute()
        return response.data
    except Exception as e:
        print(f"Error fetching from database: {e}")
        return []

def delete_project_from_db(project_id: int):
    try:
        supabase.table("user_projects").delete().eq("id", project_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting from database: {e}")
        return False
        
