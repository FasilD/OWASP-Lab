from flask import Flask, render_template, request, redirect, session
import json, os

app = Flask(__name__)
app.secret_key = 'insecure-secret-key'

DATA_FILE = 'data/users.json'

# Load users data
def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Save users data
def save_users(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Ensure data dir exists
os.makedirs('data', exist_ok=True)
users = load_users()

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])  #  FIXED
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Insecure logic: store password in plaintext, no hashing or secure auth
        if username in users:
            if users[username].get('password') != password:
                return render_template('login.html', error="Invalid credentials")
        else:
            users[username] = {"password": password, "balance": 100.0, "is_admin": False}
            save_users(users)

        session['username'] = username
        return redirect('/dashboard')

    return render_template('login.html')  # GET request

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    user = users[session['username']]
    return render_template('dashboard.html', user=session['username'], balance=user['balance'], is_admin=user['is_admin'])

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'username' not in session:
        return redirect('/')

    if request.method == 'POST':
        sender = session['username']
        recipient = request.form['recipient']
        amount = float(request.form['amount'])

        # Insecure logic flaws:
        # - No balance check
        # - No recipient existence check
        # - No input validation (e.g., negative transfer)
        # - No CSRF/session token check

        users[sender]['balance'] -= amount
        if recipient in users:
            users[recipient]['balance'] += amount
        else:
            users[recipient] = {"password": "default", "balance": amount, "is_admin": False}

        save_users(users)
        return redirect('/dashboard')

    return render_template('transfer.html')

from flask import render_template

@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
