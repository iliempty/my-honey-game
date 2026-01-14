from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = "emptynetsecret"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# قاعدة بيانات مؤقتة للمستخدمين
users = {"user@example.com": {"password": "Password123"}}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/")
def home():
    return "Welcome to Empty.net - Delivery Service"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if email in users and users[email]["password"] == password:
            user = User(email)
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials")
    return '''
        <form method="post">
            Email: <input type="text" name="email"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route("/dashboard")
@login_required
def dashboard():
    return f"Hello, {current_user.id}. Welcome to your dashboard!"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
