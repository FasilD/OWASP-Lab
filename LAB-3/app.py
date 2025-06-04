from flask import Flask, request, render_template, redirect, session
import sqlite3, os, subprocess, xml.etree.ElementTree as ET
from flask import g
import xml.etree.ElementTree as ET
from lxml import etree

app = Flask(__name__)
app.secret_key = 'supersecret'

DATABASE = 'lab.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    flag = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        try:
            conn = sqlite3.connect('lab.db')
            cur = conn.cursor()
            cur.execute(query)
            user = cur.fetchone()
            conn.close()

            if user:
                session['user'] = username
                flag = "FLAG{sql_login_bypass}"
                return render_template('dashboard.html', user=username, flag=flag)
            else:
                error = 'Invalid login'
        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html', username=session['user'])


@app.route('/initdb')
def initdb():
    conn = sqlite3.connect('lab.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comment TEXT
        )
    ''')
    conn.commit()
    conn.close()
    return ' Database initialized.'

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    result = ''
    table_status = ''
    flag = ''

    if request.method == 'POST':
        comment = request.form['comment']
        try:
            conn = sqlite3.connect('lab.db')
            cur = conn.cursor()
            #  INTENTIONALLY VULNERABLE
            sql = f"INSERT INTO feedback (comment) VALUES ('{comment}');"
            cur.executescript(sql)
            conn.commit()
        except Exception as e:
            result = f'Error: {str(e)}'
        finally:
            # Now check if the table still exists
            try:
                cur.execute("SELECT 1 FROM feedback LIMIT 1;")
                table_status = " Table 'feedback' still exists."
            except:
                table_status = " Table 'feedback' does NOT exist anymore. Visit /initdb to recreate the table."
                flag = "FLAG{stored_sql_executed}"
            conn.close()

    return render_template('feedback.html', result=result, table_status=table_status, flag=flag)


@app.route('/usersearch', methods=['GET', 'POST'])
def usersearch():
    result = ''
    flag = ''
    if request.method == 'POST':
        username = request.form['username']
        if username == '{ "$ne": null }':
            result = "User list: admin, alice, bob"
            flag = "FLAG{nosql_enum}"
        else:
            result = "No matching users found."
    return render_template('nosql.html', result=result, flag=flag)


@app.route('/lookup', methods=['GET', 'POST'])
def lookup():
    message = ''
    flag = ''
    result = ''
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        try:
            tree = etree.parse('users.xml')
            xpath_query = f'//user[username="{username}" and password="{password}"]'
            users = tree.xpath(xpath_query)
            if users:
                message = f"Welcome {username}!"
                result = 'User verified ✅'
                flag = "FLAG{xpath_bypass}"
            else:
                result = 'Invalid credentials ❌'
        except Exception as e:
            message = f"Error: {str(e)}"
    return render_template('lookup.html', message=message, result=result, flag=flag)


@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    flag = ''
    if request.method == 'POST':
        name = request.form.get('name', '')
        query = f"SELECT * FROM employees WHERE name LIKE '%{name}%'"
        try:
            conn = sqlite3.connect('lab.db')
            cur = conn.cursor()
            cur.execute(query)
            results = cur.fetchall()
            if len(results) > 1:
                flag = "FLAG{employee_info_extracted}"
        except Exception as e:
            results = [(f"Error: {str(e)}",)]
    return render_template('results.html', results=results, flag=flag)



@app.route('/ping', methods=['GET', 'POST'])
def ping():
    output = ''
    flag = ''
    if request.method == 'POST':
        target = request.form['target']
        try:
            output = subprocess.check_output(f"ping -c 1 {target}", shell=True, text=True)
            if "root" in output or "/etc/passwd" in output:
                flag = "FLAG{command_exec_pwd}"
        except subprocess.CalledProcessError as e:
            output = f"Error: {e}"
    return render_template('ping.html', output=output, flag=flag)


if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
        cur.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
        cur.execute("CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT)")
        cur.execute("INSERT INTO employees (name) VALUES ('Alice'), ('Bob'), ('Charlie')")
        cur.execute("CREATE TABLE feedback (id INTEGER PRIMARY KEY, comment TEXT)")
        conn.commit()
        conn.close()
    app.run(debug=True, host='0.0.0.0')
