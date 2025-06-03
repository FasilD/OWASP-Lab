from flask import Flask, render_template, request, redirect, url_for, make_response
from Crypto.Cipher import AES
import base64

app = Flask(__name__)

# 🚨 Hardcoded AES key (16 bytes)
SECRET_KEY = b'SECRET_KEY_12345'

def pad(s):
    pad_len = 16 - len(s) % 16
    return s + chr(pad_len) * pad_len

def unpad(s):
    return s[:-ord(s[-1])]

def encrypt(username):
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    padded = pad(username)
    encrypted = cipher.encrypt(padded.encode())
    return base64.b64encode(encrypted).decode()

def decrypt(token):
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(token))
    return unpad(decrypted.decode())

# Dummy user database
USERS = {
    "admin": "admin123",
    "user": "user123"
}

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if USERS.get(username) == password:
            token = encrypt(username)
            resp = make_response(redirect(url_for('dashboard')))
            resp.set_cookie('session', token)
            return resp
        else:
            error = 'Invalid credentials'
    return render_template('login.html', error=error)
@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('session', '', expires=0)  # Clear cookie
    return resp
    
@app.route('/dashboard')
def dashboard():
    token = request.cookies.get('session')
    if not token:
        return redirect(url_for('login'))
    try:
        username = decrypt(token)
    except:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
