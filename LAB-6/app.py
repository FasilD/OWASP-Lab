# -*- coding: utf-8 -*-
"""
A06-2021: Outdated Frameworks Vulnerabilities Lab
This Flask application is intentionally vulnerable to demonstrate common security
flaws found in outdated versions of frameworks and libraries.
FOR EDUCATIONAL PURPOSES ONLY. DO NOT USE IN PRODUCTION.
"""

from flask import Flask, request, render_template, redirect, url_for, session
import jwt # pyjwt==1.4.2 for 'none' algorithm vulnerability
import json # For pretty printing JSON in templates
import os # For conceptual RCE demo (system commands)

# --- Flask Application Setup ---
app = Flask(__name__)
# CRITICAL FOR DEBUGGER RCE DEMO: Setting debug=True.
# NEVER enable this in a production environment.
app.debug = True

# A weak secret key for session management and JWT signing (for demo purposes)
# In a real app, this should be a strong, randomly generated key stored securely.
app.config['SECRET_KEY'] = 'this_is_a_very_insecure_secret_key_for_lab_only'


# --- FLAGS ---
# These are the secret strings learners will find upon successful exploitation.
FLAG_JWT_ADMIN = "FLAG{JWT_NONE_ALGO_BYPASS_SUCCESS}"
FLAG_RCE_DEBUG = "FLAG{WERKZEUG_DEBUGGER_SHELL}"


# --- Routes for Vulnerability Demonstrations ---

@app.route('/')
def home():
    """
    Redirects to the lab index page.
    """
    return redirect(url_for('index'))

@app.route('/index')
def index():
    """
    Main lab index page, providing links to each vulnerability demo.
    """
    return render_template('index.html')


# --- Module 1: Flask 0.12 XSS via Host Header ---
@app.route('/host_xss')
def host_xss_demo():
    """
    Demonstrates XSS vulnerability in Flask 0.12 where `request.host`
    is reflected directly into the template without sufficient escaping.
    Modern Flask versions handle this more securely.
    """
    # In Flask 0.12, reflecting request.host could be vulnerable to XSS
    # if the Host header is crafted maliciously.
    # We are directly reflecting it here to demonstrate the flaw.
    malicious_host = request.headers.get('Host', 'localhost:5000')
    print(f"Received Host header for XSS demo: {malicious_host}") # For debugging/logging
    return render_template('host_xss_demo.html', host=malicious_host)


# --- Module 2: PyJWT < 1.5.0 Token Forgery (None Algorithm) ---
@app.route('/jwt_login', methods=['GET', 'POST'])
def jwt_login():
    """
    Simulates a login and demonstrates the PyJWT 'none' algorithm vulnerability.
    When an outdated PyJWT (like 1.4.2) is used, an attacker can bypass signature
    verification by setting the JWT's algorithm to 'none'.
    """
    current_token = session.get('jwt_token')
    user_data = None
    message = ""
    is_admin_flag_unlocked = False # New variable to pass to template for flag

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'login':
            username = request.form.get('username', 'guest')
            # Payload for the JWT - attacker will try to change is_admin to True
            payload = {"user": username, "is_admin": False}
            # The token is initially signed with HS256 and the app's secret key
            # The vulnerability lies in how the token is *decoded* later if not strict.
            current_token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")
            session['jwt_token'] = current_token
            message = f"Token issued for user: {username}. Try manipulating it!"

        elif action == 'clear_token':
            session.pop('jwt_token', None)
            current_token = None
            message = "Token cleared from session."

    if current_token:
        try:
            # --- VULNERABLE DECODING LOGIC ---
            # Using verify_signature=False (or an older PyJWT version that implicitly
            # accepts 'none' if not configured to disallow) is the vulnerability.
            # In a real scenario, this would be the backend logic that doesn't
            # properly verify the token's algorithm and signature.
            # We explicitly allow "none" here to demonstrate the vulnerability with `pyjwt==1.4.2`
            user_data = jwt.decode(current_token, algorithms=["HS256", "none"], verify_signature=False)
            message = f"Token decoded (signature NOT verified for demo). User: {user_data.get('user')}, Admin: {user_data.get('is_admin')}"
            print(f"Decoded user data for JWT demo: {user_data}")

            # Check if admin flag should be unlocked based on 'is_admin' field in the *decoded* payload
            if user_data.get('is_admin') is True:
                is_admin_flag_unlocked = True

        except jwt.ExpiredSignatureError:
            message = "Error: Token has expired."
        except jwt.InvalidTokenError:
            message = "Error: Invalid token."
        except Exception as e:
            message = f"Error decoding token: {e}. Token might be malformed or invalid."
            print(f"JWT decoding error: {e}")
    else:
        message = "No token in session. Please login to generate one."

    return render_template('jwt_demo.html',
                           token=current_token,
                           user_data=json.dumps(user_data, indent=2) if user_data else "None",
                           message=message,
                           is_admin_flag_unlocked=is_admin_flag_unlocked, # Pass flag status
                           jwt_admin_flag=FLAG_JWT_ADMIN) # Pass the flag value


# --- Module 3: Werkzeug < 0.11.11 Debugger Remote Code Execution (RCE) ---
@app.route('/debug_rce')
def debug_rce_demo():
    """
    Provides a page for the Werkzeug debugger RCE demonstration.
    The application is running with app.debug = True, which enables the debugger
    on uncaught exceptions.
    """
    return render_template('debug_rce_demo.html', rce_flag=FLAG_RCE_DEBUG)

@app.route('/trigger_error')
def trigger_error():
    """
    This route intentionally raises an exception to activate the Werkzeug debugger.
    If `app.debug` is True, an interactive debugger will appear in the browser.
    """
    print("Attempting to trigger an intentional error for debugger demo...")
    # Intentionally raise a "ZeroDivisionError" to bring up the debugger
    # In a real scenario, any unhandled exception would do this.
    result = 1 / 0
    return f"This text should not be seen if debugger activates: {result}"


# --- Main Application Run ---
if __name__ == '__main__':
    # When running in a lab environment, use 0.0.0.0 to make it accessible
    # from other VMs on the same host-only network if needed, or from the host.
    # For strictest isolation, keep it to 127.0.0.1 and access from within VM.
    app.run(host='0.0.0.0', port=5000)

