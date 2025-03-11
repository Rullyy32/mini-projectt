from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
app = Flask(__name__)

app.secret_key = 'supersentimentalsecrettheory'

def create_db():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS profile (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    bmi REAL NOT NULL,
                    height REAL NOT NULL,
                    weight REAL NOT NULL,
                    disease_history TEXT NOT NULL,
                    category TEXT)''')
    conn.commit()
    conn.close()

create_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('user.db')
        c = conn.cursor()

        try:
            c.execute("SELECT * FROM user WHERE email = ?", (email,))

            if c.fetchone():
                flash('Email is already registered!', 'error')
            else:
                c.execute("INSERT INTO user (name, email, password) VALUES (?, ?, ?)", (name, email, password))
                conn.commit()
                flash('Register successful!', 'success')
                return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Error : Failed to save data', 'error')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with sqlite3.connect('user.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM user WHERE email = ? AND password = ?", (email, password))
            user = c.fetchone()

        if user:
            return redirect(url_for('profile'))
        else:
            flash('Invalid Email or Password!', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == "POST":
        name = request.form["name"]
        age = int(request.form["age"])
        height = int(request.form["height"]) / 100
        weight = int(request.form["weight"])
        disease_history = request.form["disease_history"]

        bmi = weight / (height * height)

        if bmi < 18.5:
            category = "Underweight"
            # pesan = "BMI Anda rendah, coba tingkatkan asupan kalori."
            pesan = "Your Body Mass Index is low, try increasing your calorie intake."
            warna = "warning"
        elif bmi < 25:
            category = "Normal"
            # pesan = "BMI Anda ideal, pertahankan pola hidup sehat!"
            pesan = "Your Body Mass Index is ideal, maintain a healthy lifestyle!"
            warna = "success"
        else:
            category = "Overweight"
            # pesan = "BMI Anda cukup tinggi, coba perhatikan pola makan dan olahraga."
            pesan = "Your Body Mass Index is quite high, try paying attention to your diet and exercise."
            warna = "danger"

        with sqlite3.connect("user.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                    INSERT INTO profile (name, age, height, weight, disease_history, bmi, category)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (name, age, height, weight, disease_history, bmi, category))
            conn.commit()

            flash(f"Category: {category} (BMI: {bmi:.2f}) — {pesan}", warna)
            return redirect(url_for("choose"))

    return render_template('profile.html')

@app.route('/choose')
def choose():
    return render_template('choose.html')

@app.route('/beginner')
def beginner():
    return render_template('beginner.html')

@app.route('/basic')
def basic():
    return render_template('basic.html')

@app.route('/pro')
def pro():
    return render_template('pro.html')

@app.route('/premium')
def premium():
    return render_template('premium.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')