from flask import Flask, request, session, redirect, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError

app = Flask(__name__)
app.secret_key = 'qstate-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# ----------------- Models ------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    role = db.Column(db.String(20))  # user/admin

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    content = db.Column(db.String(255))

# ----------------- Routes ------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/initdb')
def initdb():
    db.drop_all()
    db.create_all()
    db.session.add_all([
        User(username='alice', password='alice123', role='user'),
        User(username='bob', password='bob123', role='admin')
    ])
    db.session.add_all([
        Message(user_id=1, content="Alice's secret message."),
        Message(user_id=2, content="Bob's private message.")
    ])
    db.session.commit()
    return "Database initialized."

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            user = User.query.filter_by(
                username=request.form['username'],
                password=request.form['password']
            ).first()
            if user:
                session['user_id'] = user.id
                session['role'] = user.role
                return redirect('/dashboard')
            else:
                error = "Invalid username or password"
        except OperationalError:
            error = "Internal server error: please contact the administrator."
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    user = User.query.get(session['user_id'])

    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ----------------- OWASP Vulnerable Scenarios ------------------

#  Scenario 1: IDOR (Insecure Direct Object Reference)
@app.route('/message/<int:msg_id>')
def view_message(msg_id):
    if 'user_id' not in session:
        return redirect('/login')
    #  No ownership check — vulnerable to IDOR
    message = Message.query.get(msg_id)
    if not message:
        return "Message not found", 404
    return f"Message #{msg_id}: {message.content}"

#  Scenario 2: Function-Level Access Control Bypass
@app.route('/admin')
def admin_panel():
    if 'user_id' not in session:
        return redirect('/login')
    #  No role check — any logged-in user can access
    return "<h1>Admin Control Panel</h1><p>This should be protected by role, but it's not.</p>"

#  Scenario 3: Forceful Browsing
@app.route('/hidden-report')
def hidden_report():
    #  No auth or role check — exposed via direct URL
    return "<h2>Confidential report</h2><p>This sensitive data should be protected.</p>"

#  Scenario 4: Role Tampering
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect('/login')
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        user.username = request.form['username']
        user.role = request.form['role']  #  User can change their own role
        db.session.commit()
        return redirect('/dashboard')
    return render_template('edit_profile.html', user=user)

# ------------------ Run -------------------
if __name__ == '__main__':
    app.run(debug=True)
