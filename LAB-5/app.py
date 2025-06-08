# LAB-5/app.py

import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import logging
from functools import wraps # For authentication decorator

app = Flask(__name__)

# --- VULNERABLE VERSION: Debug Mode Enabled & Weak Secret Key ---
# This enables verbose error messages (Vulnerability 2) and is not secure for production.
app.debug = True
# A weak/hardcoded secret key (Security Misconfiguration - often related to A05 too)
app.secret_key = 'super_secret_dev_key_do_not_use_in_prod'
# --- END VULNERABLE VERSION ---

# --- SECURE VERSION: Debug Mode Disabled & Strong Secret Key (Remediation Opportunity) ---
# To remediate, comment out the two lines above (app.debug and app.secret_key)
# and uncomment the following lines.
# app.debug = False # Disable debug mode in production to prevent verbose errors.
# app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_fallback_secret_for_dev_if_env_not_set')
# if app.secret_key == 'default_fallback_secret_for_dev_if_env_not_set':
#     print("WARNING: Using a fallback secret key. Set FLASK_SECRET_KEY environment variable in production!")
# --- END SECURE VERSION ---


# Configure logging to capture output (Vulnerability 6 & Remediation)
log_format = '%(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)
# Set logging level for werkzeug (Flask's internal WSGI server) to WARNING to reduce noise
logging.getLogger('werkzeug').setLevel(logging.WARNING)

# --- VULNERABLE VERSION: Hardcoded Credentials (Vulnerability 1) ---
VULNERABLE_ADMIN_USERNAME = "admin"
VULNERABLE_ADMIN_PASSWORD = "password123"
# --- END VULNERABLE VERSION ---

# --- SECURE VERSION: Credentials from Environment Variables (Remediation Opportunity) ---
# To remediate, comment out the two VULNERABLE_ADMIN lines above
# and uncomment the following lines.
# SECURE_ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "secure_admin_user")
# SECURE_ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "secure_admin_pass_123")
# if SECURE_ADMIN_USERNAME == "secure_admin_user" or SECURE_ADMIN_PASSWORD == "secure_admin_pass_123":
#     print("WARNING: Using default secure credentials. Ensure ADMIN_USERNAME and ADMIN_PASSWORD env vars are set securely!")
# --- END SECURE VERSION ---


# --- SECURE VERSION: Authentication Decorator (Part of Remediation 1) ---
# This decorator is for the admin panel to ensure authenticated access
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'logged_in' not in request.session:
#             return redirect(url_for('login'))
#         return f(*args, **kwargs)
#     return decorated_function
# --- END SECURE VERSION ---


# --- SECURE VERSION: Custom Error Handler (Remediation for Vulnerability 2) ---
# To remediate verbose errors, uncomment this block.
# @app.errorhandler(500)
# def internal_server_error(e):
#     # Log the actual error, but don't show it to the user
#     app.logger.error(f"Internal Server Error: {e}")
#     return render_template('error.html', error_message="An unexpected error occurred. Please try again later."), 500
# --- END SECURE VERSION ---


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # --- VULNERABLE VERSION: Overly Verbose Logging (Vulnerability 6) & Hardcoded Credentials (Vulnerability 1) ---
        app.logger.warning(f"Attempting login for user '{username}'. Provided password: '{password}'") # Logs sensitive info
        if username == VULNERABLE_ADMIN_USERNAME and password == VULNERABLE_ADMIN_PASSWORD:
            flash("Login successful!")
            # In a real app, you'd set a session cookie here
            # request.session['logged_in'] = True # Placeholder for actual session management
            return redirect(url_for('admin_panel'))
        else:
            message = "Invalid credentials. Please try again."
        # --- END VULNERABLE VERSION ---

        # --- SECURE VERSION: Secure Logging & Env Variable Credentials (Remediation Opportunity) ---
        # To remediate, comment out the VULNERABLE VERSION block above and uncomment the following.
        # app.logger.warning(f"Failed login attempt for user '{username}'.") # No sensitive info in logs
        # if username == SECURE_ADMIN_USERNAME and password == SECURE_ADMIN_PASSWORD:
        #     flash("Login successful to Secure Admin Panel!")
        #     # In a real app, you'd set a session cookie here
        #     # request.session['logged_in'] = True # Placeholder for actual session management
        #     return redirect(url_for('admin_panel'))
        # else:
        #     message = "Invalid credentials. Please try again."
        # --- END SECURE VERSION ---

    return render_template('login.html', message=message)

@app.route('/admin')
# --- VULNERABLE VERSION: No Authentication Required for Admin Panel (Implicit Vulnerability 1) ---
def admin_panel():
    # Flag for Default/Hardcoded Credentials (Vulnerability 1)
    flag_default_creds = "FLAG{DEFAULT_CREDS_EASY_ACCESS_TO_ADMIN}"
    return render_template('admin_panel.html', flag=flag_default_creds)
# --- END VULNERABLE VERSION ---

# --- SECURE VERSION: Authentication Required for Admin Panel (Remediation Opportunity) ---
# To remediate, comment out the VULNERABLE admin_panel function above
# and uncomment the following. Also ensure 'login_required' decorator is uncommented above.
# @app.route('/admin')
# #@login_required # Uncomment this after you implement session management
# def admin_panel():
#     # Flag becomes inaccessible without proper authentication
#     return render_template('admin_panel.html', flag="Admin Panel is now secure. Flag is only accessible via secure authentication.")
# --- END SECURE VERSION ---


@app.route('/broken')
def broken_page():
    # --- VULNERABLE VERSION: Triggers a verbose error (Vulnerability 2) ---
    # This intentionally causes an error to demonstrate verbose error messages.
    # Flag for Verbose Error Messages (Vulnerability 2)
    result = 1 / 0  # This will cause a ZeroDivisionError
    return f"This line will not be reached. Flag: FLAG{{DEBUG_LEAKS_INFO}} "
    # --- END VULNERABLE VERSION ---

# --- SECURE VERSION: 'broken_page' will now show generic error if debug is off ---
# No change needed here for remediation, as the error handler (if uncommented) will catch it.
# --- END SECURE VERSION ---


# --- VULNERABLE VERSION: Sensitive File Exposure (Vulnerability 3) ---
@app.route('/configs/<path:filename>')
def serve_configs(filename):
    # This route directly serves files from the 'configs' directory.
    # A pentester would look for sensitive files here.
    return send_from_directory('configs', filename)
# --- END VULNERABLE VERSION ---

# --- SECURE VERSION: Remove Sensitive File Exposure Route (Remediation Opportunity) ---
# To remediate, simply comment out or delete the entire '/configs/<path:filename>' route above.
# --- END SECURE VERSION ---


# --- VULNERABLE VERSION: Unnecessary Features/Default Files Exposed (Vulnerability 4) ---
@app.route('/admins/<path:filename>')
def serve_default_admin_files(filename):
    # This route exposes a directory that might contain unnecessary default admin files.
    # A pentester would check for files like 'default_admin_report.txt'.
    return send_from_directory('admins', filename)
# --- END VULNERABLE VERSION ---

# --- SECURE VERSION: Remove Unnecessary Features Route (Remediation Opportunity) ---
# To remediate, simply comment out or delete the entire '/admins/<path:filename>' route above.
# Also, physically remove or move sensitive files from this directory.
# --- END SECURE VERSION ---


# --- SECURE VERSION: Add Security Headers (Remediation for Vulnerability 5) ---
# To remediate, uncomment the following block.
# @app.after_request
# def add_security_headers(response):
#     response.headers['X-Content-Type-Options'] = 'nosniff'
#     response.headers['X-Frame-Options'] = 'DENY'
#     # HSTS should only be enabled on HTTPS. For local HTTP lab, be cautious.
#     # response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
#     response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;"
#     response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'
#     # Add cache control headers to prevent caching sensitive data
#     response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
#     response.headers['Pragma'] = 'no-cache'
#     response.headers['Expires'] = '0'
#     return response
# --- END SECURE VERSION ---


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)