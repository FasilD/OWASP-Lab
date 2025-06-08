# OWASP A05:2021 – Security Misconfiguration Lab: Testing Guide & Remediation Exercise

This guide provides step-by-step instructions for testing the various security misconfigurations demonstrated in the Flask application. It covers both the **Vulnerable Version** and how to verify the **Secure Version** after applying remediations. **Your task as a learner is to find the flags and then apply the remediations yourself.**

**Before You Start:**

* This app is dockernized app if you wish to use docker ensure you have Docker Desktop installed and running.
* Navigate to the `LAB-5` directory in your terminal.

* **To start the VULNERABLE VERSION:** 
Run 
```
python3 app.py
or
sudo docker-compose up --build.
```
* **For Remediation:** You will modify `app.py` (and potentially other files as instructed) to implement the "SECURE VERSION" changes, then rerun the app or rebuild and restart the Docker container 
* Run 
```
ctrl + c # to stop the app
python3 app.py
or
docker-compose up --build
```

## **I. Testing the VULNERABLE VERSION (Find the Flags!)**

Start the application with the vulnerable configurations: 

```
python3 app.py
or
docker-compose up --build
```

### 1. Default/Hardcoded Credentials (Vulnerability 1)

* **Vulnerability:** The application uses easily guessable/default admin credentials.
* **Real-Life Impact:** Unauthorized administrative access, leading to data breaches, system compromise, or further lateral movement.
* **Pentester Focus:** Identify all systems, services, and accounts using default or hardcoded credentials. Check common defaults, source code, and configuration files.

**Testing Steps:**

1.  **Open Browser:** Navigate to `http://localhost:5000/login`.
2.  **Attempt Login:**
    * Enter `Username: admin`
    * Enter `Password: password123`
3.  **Observe Result:** You should be successfully logged in and redirected to the "Admin Panel" page (`/admin`).
4.  **Find the Flag:** The flag for this vulnerability will be displayed directly on the `/admin` page upon successful login.
    * **FLAG:** `FLAG{DEFAULT_CREDS_EASY_ACCESS_TO_ADMIN}`

### 2. Verbose Error Messages (Vulnerability 2)

* **Vulnerability:** Debug mode is enabled, revealing detailed stack traces on errors.
* **Real-Life Impact:** Information leakage (file paths, variable names, system details) that aids attackers in understanding the application's structure, versions, and potential weaknesses.
* **Pentester Focus:** Trigger diverse errors to maximize information leakage. Look for absolute paths, database errors, framework versions, and internal function calls that can be used for further exploitation.

**Testing Steps:**

1.  **Open Browser:** Navigate to `http://localhost:5000/broken`.
2.  **Observe Result:** Instead of a generic error, you should see a full Python `ZeroDivisionError` stack trace in your browser, including paths like `app.py` and the exact line number where the error occurred.
3.  **Find the Flag:** The flag will be part of the verbose error message, specifically near where the `1 / 0` operation is attempted.
    * **FLAG:** `FLAG{DEBUG_LEAKS_INFO}`

### 3. Sensitive File Exposure (Vulnerability 3)

* **Vulnerability:** Critical configuration files or application source code are accessible via direct URL paths.
* **Real-Life Impact:** Leakage of API keys, database credentials, internal logic, or other secrets, leading to direct compromise.
* **Pentester Focus:** Systematically probe for common configuration file names, backup files (`.bak`, `.old`, `.zip`), source code files (`.py.txt`, `.php.bak`), and version control system files (`.git/config`, `.svn/entries`). Understand the *type* of sensitive data exposed (credentials, PII, intellectual property).

**Testing Steps:**
**You can use directory brut forcing to discover vulnerable files**
1.  **Open Browser (Sensitive Config File):** Navigate to `http://localhost:5000/configs/config.py`.
2.  **Observe Result:** You should see the plaintext content of `config.py`.
3.  **Find the Flag:** Locate the `API_KEY` variable in `config.py`.
    * **FLAG:** `FLAG{EXPOSED_CONFIG_SECRET}`
### 4. Unnecessary Features/Default Files Exposed (Vulnerability 4)

* **Vulnerability:** Default administrative reports or sample files are left on the server and are publicly accessible.
* **Real-Life Impact:** Unauthorized access to internal documents, user lists, internal network details, or other sensitive information, increasing the attack surface.
* **Pentester Focus:** Identify the application's framework and web server to research known default files, directories, and administrative interfaces that should be removed or secured in a production environment.

**Testing Steps:**
**Brute forcing**
1.  **Open Browser:** Navigate to `http://localhost:5000/admins/report.txt`.
2.  **Observe Result:** You should see the plaintext content of the "Confidential Admin Report."
3.  **Find the Flag:** The flag is embedded directly within the content of report.txt`.
    * **FLAG:** `FLAG{UNNECESSARY_FEATURE_FOUND}`

### 5. Lack of Security Headers (Vulnerability 5)

* **Vulnerability:** Essential HTTP security headers are missing, leaving the application vulnerable to client-side attacks (e.g., Clickjacking, MIME-sniffing, XSS exploitation).
* **Real-Life Impact:** Browser-based attacks that can compromise user sessions, steal data, or trick users into performing unintended actions.
* **Pentester Focus:** Systematically check for the presence and correct configuration of all standard security headers on *every* response. Their absence indicates a weakened defense against common client-side exploits.

**Testing Steps:**

1.  **Open Browser:** Navigate to `http://localhost:5000/` (or any other page).
2.  **Open Developer Tools:** Press `F12` (or right-click and select "Inspect" or "Inspect Element") to open your browser's developer tools.
3.  **Go to Network Tab:** Select the "Network" tab.
4.  **Refresh Page:** Refresh the page (`Ctrl+R` or `Cmd+R`).
5.  **Examine Main Request:** Click on the `localhost:5000` (or `index.html`) request in the Network tab.
6.  **View Headers:** Look at the "Headers" sub-tab, specifically the "Response Headers" section.
7.  **Observe Missing Headers:** You should **not** see the following critical headers:
    * `X-Content-Type-Options`
    * `X-Frame-Options`
    * `Strict-Transport-Security` (HSTS)
    * `Content-Security-Policy` (CSP)
    * `Referrer-Policy`
    * `Cache-Control`, `Pragma`, `Expires` (for sensitive pages)
    * **FLAG:** The *absence* of these headers is the flag in itself for this vulnerability. Document which ones are missing.

### 6. Overly Verbose Logging (Vulnerability 6)

* **Vulnerability:** The application logs sensitive information (like plaintext passwords) to its console/logs.
* **Real-Life Impact:** If an attacker gains access to logs (e.g., via log server compromise, or Remote Code Execution), they can harvest credentials, PII, or other critical data.
* **Pentester Focus:** Identify all logging points in the application. Trigger events that would generate logs, then look for any sensitive data (credentials, session IDs, PII, internal IP addresses, API keys) that should never be written to logs.

**Testing Steps:**

1.  **Go to Login Page:** Navigate to `http://localhost:5000/login`.
2.  **Attempt Failed Login:**
    * Enter `Username: testuser`
    * Enter `Password: wrongpassword`
    * Click "Login".
3.  **Check Docker Logs:** Switch to your terminal where `docker-compose up` is running.
4.  **Observe Sensitive Log:** You should see a `WARNING` entry similar to:
    `WARNING - Attempting login for user 'testuser'. Provided password: 'wrongpassword'`
5.  **Find the Flag:** The flag is implicitly found by observing the sensitive data (the plaintext password) in the logs. You can consider `FLAG{LOGGED_SENSITIVE_DATA}` to be discovered upon seeing the password.
    * **FLAG:** `FLAG{LOGGED_SENSITIVE_DATA}` (Identified by observing the plaintext password in logs).

## **II. Remediation Exercise (Make it Secure!)**

Now that you've found all the flags and understood the vulnerabilities, it's time to fix them. Your goal is to apply the "SECURE VERSION" code in `app/app.py` and `docker-compose.yml`, and verify the remediations using the steps below.

**Remediation Steps:**

1.  **Open `app.py` in your text editor.**
2.  For each vulnerability section (commented as `--- VULNERABLE VERSION ---` and `--- SECURE VERSION ---`):
    * **Comment out or delete** the "VULNERABLE VERSION" code block.
    * **Uncomment** the corresponding "SECURE VERSION" code block.
    * **Pay attention to instructions** within the comments (e.g., setting environment variables, removing entire routes, or uncommenting decorators).
3.  **(Optional but Recommended for full remediation):** Open `docker-compose.yml`.
    * Uncomment(if it is necessary) the `environment:` section under the `web` service. This will set the `ADMIN_USERNAME` and `ADMIN_PASSWORD` environment variables that the secure version of `app.py` will use.
    * Add `FLASK_SECRET_KEY: "your_long_random_secret_key_here"` to the environment variables for `app.secret_key`.
4.  **Remove Exposed Files:**
    * Physically delete or move `/configs/config.py`.
    * Physically delete or move `/admins/report.txt`.
    * It's also good practice to physically remove `/configs/app.py` if it was there for demonstration, as source code should not be in public directories.
5.  **Rebuild and Restart Docker:**
    * In your terminal, stop the running containers: `docker-compose down`
    * Rebuild and restart the containers with the new changes: `docker-compose up --build`

## **III. Testing the SECURE VERSION (Verify Remediations)**

After applying the remediations and restarting Docker, perform these steps to ensure the vulnerabilities are fixed.
### 1. Default/Hardcoded Credentials (Remediation Verification)

* **Remediation:** Admin credentials are now strong and pulled from environment variables, no longer hardcoded or default.
* **Expected Result:** Old credentials fail, new secure credentials (from `docker-compose.yml`) work.

**Testing Steps:**

1.  **Open Browser:** Navigate to `http://localhost:5000/login`.
2.  **Attempt Old Login (Expected Fail):**
    * Enter `Username: admin`
    * Enter `Password: password123`
    * **Observe Result:** Login should *fail*, and you should see "Invalid credentials. Please try again." The previous flag should be inaccessible.
3.  **Attempt New Secure Login (Expected Success):**
    * Refer to `docker-compose.yml` for the new secure credentials:
        * `Username: secure_admin_user`
        * `Password: secure_admin_pass_123`
    * Enter these credentials and click "Login".
    * **Observe Result:** You should now be successfully logged in to the "Secure Admin Panel." (The flag will no longer be shown on the secure admin panel).

### 2. Verbose Error Messages (Remediation Verification)

* **Remediation:** Debug mode is disabled, and a custom error handler is in place.
* **Expected Result:** Generic error pages, no stack traces or sensitive information.

**Testing Steps:**

1.  **Open Browser:** Navigate to `http://localhost:5000/broken`.
2.  **Observe Result:** You should now see the generic "Oops! Something went wrong." error page (`error.html`), with no stack trace or sensitive details. The previous flag should be hidden.
### 3. Sensitive File Exposure (Remediation Verification)

* **Remediation:** The routes allowing direct access to sensitive files have been removed, and the files are physically removed/moved.
* **Expected Result:** 404 Not Found errors for these paths.

**Testing Steps:**

1.  **Open Browser (Sensitive Config):** Navigate to `http://localhost:5000/configs/config.py`.
2.  **Observe Result:** You should receive a "404 Not Found" error. The flag should be inaccessible.
3.  **Open Browser (Application Source):** Navigate to `http://localhost:5000/configs/app.py`.
4.  **Observe Result:** You should also receive a "404 Not Found" error. The flag should be inaccessible.

### 4. Unnecessary Features/Default Files Exposed (Remediation Verification)

* **Remediation:** The route serving the default admin report has been removed, and the file is physically removed/moved.
* **Expected Result:** 404 Not Found error for the report.

**Testing Steps:**

1.  **Open Browser:** Navigate to `http://localhost:5000/admins/report.txt`.
2.  **Observe Result:** You should receive a "404 Not Found" error. The flag should be inaccessible.

### 5. Implementation of Security Headers (Remediation Verification)

* **Remediation:** Essential HTTP security headers are now included in every response.
* **Expected Result:** The presence of critical security headers.

**Testing Steps:**

1.  **Open Browser:** Navigate to `http://localhost:5000/` (or any other page).
2.  **Open Developer Tools:** Press `F12` to open your browser's developer tools.
3.  **Go to Network Tab:** Select the "Network" tab.
4.  **Refresh Page:** Refresh the page.
5.  **Examine Main Request:** Click on the `localhost:5000` (or `index.html`) request in the Network tab.
6.  **View Headers:** Look at the "Headers" sub-tab, specifically the "Response Headers" section.
7.  **Observe Added Headers:** You should now see the following headers present:
    * `X-Content-Type-Options: nosniff`
    * `X-Frame-Options: DENY`
    * `Content-Security-Policy: ...` (with a suitable policy)
    * `Referrer-Policy: no-referrer-when-downgrade`
    * `Cache-Control: no-store, no-cache, must-revalidate, max-age=0` (and related caching headers)
    * *(Optional, if you uncommented HSTS): `Strict-Transport-Security`*

### 6. Overly Verbose Logging (Remediation Verification)

* **Remediation:** Sensitive information (like plaintext passwords) is no longer logged.
* **Expected Result:** Login failure warnings without plaintext passwords.

**Testing Steps:**

1.  **Go to Login Page:** Navigate to `http://localhost:5000/login`.
2.  **Attempt Failed Login:**
    * Enter `Username: testuser`
    * Enter `Password: wrongpassword`
    * Click "Login".
3.  **Check Docker Logs:** Switch to your terminal where `docker-compose up` is running.
4.  **Observe Remediation:** You should now see a `WARNING` entry similar to:
    `WARNING - Failed login attempt for user 'testuser'.`
    **Crucially, the plaintext password should *not* be present in the log. The flag `FLAG{LOGGED_SENSITIVE_DATA}` should no longer be evident.**

**Congratulations!** You have successfully exploited the security misconfigurations, found the hidden flags, and applied the necessary remediations to secure the Flask application. This hands-on experience provides a clear understanding of OWASP A05:2021 and the importance of secure configuration.