import os
import asyncio
import threading
from fastapi import FastAPI, Request, HTMLResponse, RedirectResponse, Form
import uvicorn

# استيراد إعدادات البوت والملفات الخاصة بك (تأكد من توافقها مع مشروعك)
# from bot import dp, bot  (استبدلها بما يناسب كودك الأصلي لتشغيل البوت)

app = FastAPI()

# كلمة المرور للوحة التحكم تسحب من إعدادات المنصة (Secrets)
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head><title>Webs Bot Status</title></head>
        <body style="background: #0f172a; color: #fff; font-family: Arial; text-align: center; padding-top: 100px;">
            <h2>🚀 Webs Bot is Running 24/7 on Fly.io!</h2>
            <p>البوتيعمل الآن بشكل مستمر مع لوحة التحكم.</p>
            <a href="/admin" style="background: #3b82f6; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">تسجيل الدخول للوحة التحكم</a>
        </body>
    </html>
    """

@app.get("/admin", response_class=HTMLResponse)
async def admin_login_page():
    return """
    <html>
        <head><title>Admin Login</title></head>
        <body style="background: #0f172a; color: #fff; font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
            <form method="post" action="/admin/login" style="background: #1e293b; padding: 30px; border-radius: 10px; width: 300px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                <h3>Admin Panel Login</h3>
                <input type="password" name="password" placeholder="أدخل كلمة المرور" required style="width: 100%; padding: 10px; margin: 10px 0; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 5px; box-sizing: border-box;" />
                <button type="submit" style="width: 100%; padding: 10px; background: #22c55e; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">دخول</button>
            </form>
        </body>
    </html>
    """

@app.post("/admin/login")
async def handle_login(password: str = Form(...)):
    if password == ADMIN_PASSWORD:
        response = RedirectResponse(url="/admin/dashboard", status_code=303)
        response.set_cookie(key="auth", value="true")
        return response
    return "كلمة المرور غير صحيحة", 403

@app.get("/admin/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if request.cookies.get("auth") != "true":
        return RedirectResponse(url="/admin", status_code=303)
    return """
    <html>
        <head><title>Admin Dashboard</title></head>
        <body style="background: #0f172a; color: #fff; font-family: Arial; padding: 40px;">
            <div style="background: #1e293b; padding: 30px; border-radius: 10px;">
                <a href="/admin" style="color: #ef4444; float: left; text-decoration: none;">تسجيل الخروج</a>
                <h2>📊 لوحة تحكم البوت</h2>
                <hr style="border-color: #334155;">
                <p>أهلاً بك! السيرفر يعمل بكفاءة تامة على Fly.io وقاعدة البيانات مرتبطة بنجاح.</p>
            </div>
        </body>
    </html>
    """

def run_server():
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    # تشغيل سيرفر الويب في خلفية الكود لترضى منصة Fly.io ويبقى البوت شغالاً
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    print("Bot & Web Server are starting...")
    
    # -------------------------------------------------------------
    # ضع كود تشغيل بوت تيليجرام الخاص بك هنا (مثلاً: asyncio.run(main()))
    # -------------------------------------------------------------
