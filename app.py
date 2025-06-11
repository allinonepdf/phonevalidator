from flask import Flask, request, render_template, redirect, url_for, session, send_file
import requests
import os
import pandas as pd
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['LOG_FOLDER'] = 'logs'

NUMVERIFY_API_KEY = "e2a124b534c2404e935181df56541bec"
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"}
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "admin":
            return "Access Denied", 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = USERS.get(username)
        if user and user['password'] == password:
            session['user'] = username
            session['role'] = user['role']
            return redirect(url_for('home'))
        else:
            error = "Invalid credentials"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    result = {}
    if request.method == 'POST' and 'phone' in request.form:
        number = request.form['phone']
        result = validate_phone(number)
        log_action("single", number, result)
    return render_template('index.html', result=result)

@app.route('/bulk', methods=['GET', 'POST'])
@login_required
def bulk():
    results = []
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            df = pd.read_csv(filepath)
            numbers = df['phone'].dropna().astype(str)
            for number in numbers:
                data = validate_phone(number)
                log_action("bulk", number, data)
                results.append(data)
            df_results = pd.DataFrame(results)
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'bulk_results.csv')
            df_results.to_csv(output_path, index=False)
            return send_file(output_path, as_attachment=True)
    return render_template('bulk.html', results=results)

@app.route('/admin/logs')
@login_required
@admin_required
def view_logs():
    log_files = os.listdir(app.config['LOG_FOLDER'])
    log_content = {}
    for file in log_files:
        with open(os.path.join(app.config['LOG_FOLDER'], file)) as f:
            log_content[file] = f.readlines()
    return render_template('admin.html', logs=log_content)

# Placeholder for Google Login route
@app.route('/google-login')
def google_login():
    return "Google Login not implemented in this local version"

def validate_phone(number):
    url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={number}"
    response = requests.get(url)
    return response.json()

def log_action(action_type, number, result):
    log_file = os.path.join(app.config['LOG_FOLDER'], f"{datetime.now().date()}_log.txt")
    with open(log_file, "a") as f:
        f.write(f"{datetime.now()}	{action_type}	{number}	{result.get('carrier')}	{result.get('line_type')}
")

if __name__ == '__main__':
    app.run(debug=True)
