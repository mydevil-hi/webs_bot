import os
import asyncio
import threading
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn

app = FastAPI()

# كلمة المرور للوحة التحكم (تسحب من المتغيرات السرية في Fly.io)
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <meta charset="utf-8">
            <title>Webs Bot Panel</title>
            <style>
                body { background: #0f172a; color: #f8fafc; font-family: Arial, sans-serif; text-align: center; padding-top: 100px; }
                .card { background: #1e293b; padding: 30px; border-radius: 10px; display: inline-block; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
                a { background: #3b82f6; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 15px; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>🚀 Webs Bot is Online</h2>
                <p>البوتيعمل الآن بشكل مستمر على Fly.io</p>
                <a href="/admin">تسجيل الدخول لوحة التحكم</a>
            </div>
        </body>
    </html>
    """

@app.get("/admin", response_class=HTMLResponse)
async def admin_login():
    return """
    <html>
        <head>
            <meta charset="utf-8">
            <title>Admin Login</title>
            <style>
                body { background: #0f172a; color: #f8fafc; font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                .login-box { background: #1e293b; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); width: 300px; }
                input { width: 100%; padding: 10px; margin: 10px 0; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 5px; box-sizing: border-box; }
                button { width: 100%; padding: 10px; background: #22c55e; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="login-box">
                <h3>Admin Panel</h3>
                <form method="post" action="/admin/login">
                    <input type="password" name="password" placeholder="أدخل كلمة المرور" required />
                    <button type="submit">دخول</button>
                </form>
            </div>
        </body>
    </html>
    """

@app.post("/admin/login")
async def handle_login(password: str = Form(...)):
    if password == ADMIN_PASSWORD:
        response = RedirectResponse(url="/admin/dashboard", status_code=303)
        response.set_cookie(key="auth", value="true")
        return response
    raise HTTPException(status_code=403, detail="كلمة المرور غير صحيحة")

@app.get("/admin/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if request.cookies.get("auth") != "true":
        return RedirectResponse(url="/admin", status_code=303)
    return """
    <html>
        <head>
            <meta charset="utf-8">
            <title>Dashboard</title>
            <style>
                body { background: #0f172a; color: #f8fafc; font-family: Arial, sans-serif; padding: 40px; }
                .container { background: #1e293b; padding: 30px; border-radius: 10px; }
                .logout { color: #ef4444; text-decoration: none; float: left; }
            </style>
        </head>
        <body>
            <div class="container">
                <a href="/admin" class="logout">تسجيل الخروج</a>
                <h2>📊 لوحة تحكم البوت</h2>
                <hr style="border-color: #334155;">
                <p>مرحباً بك! السيرفر يعمل بكفاءة وتم ربط قاعدة البيانات بنجاح.</p>
            </div>
        </body>
    </html>
    """

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    # تشغيل سيرفر الويب في خلفية الكود لترضى منصة Fly.io
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # هنا يتم تشغيل كود بوت التيليجرام الخاص بك (مثل aiogram long polling)
    print("Bot & Web Server are starting...")
    # ضع هنا كود تشغيل البوت الخاص بك ليبقى يعمل بالتوازي
    # مثال: asyncio.run(main_bot())
    
