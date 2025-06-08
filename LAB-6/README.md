# A06-2021: Outdated Frameworks Vulnerabilities Lab

This lab is designed to provide hands-on experience with common vulnerabilities found in outdated versions of popular Python web frameworks and libraries. You'll explore **Cross-Site Scripting (XSS)** via Host header injection in Flask, **JWT token forgery** using the "none" algorithm in PyJWT, and **Remote Code Execution (RCE)** through an exposed Werkzeug debugger.
## **Important Safety Warnings**

- **ISOLATED ENVIRONMENT REQUIRED:** You **MUST** run this lab within a virtual machine (VM) like VirtualBox or VMware. Configure the VM's network adapter to be on a "Host-Only" or "Internal" network, ensuring it has **NO** internet access and is isolated from your main system.
    
- **EDUCATIONAL PURPOSES ONLY:** The techniques demonstrated here are for learning and understanding cybersecurity vulnerabilities. **NEVER** attempt these actions on any system you don't own or have explicit, written permission to test. Unauthorized access is illegal and unethical.
    
- **DO NOT USE IN PRODUCTION:** The application provided is intentionally vulnerable. **NEVER** deploy or use any part of this code in a production or publicly accessible environment.
    
- **TAKE VM SNAPSHOTS:** Before starting the lab, take a snapshot of your virtual machine. This allows you to easily revert to a clean state if you encounter issues or wish to repeat an exercise.
## **Lab Setup Instructions**

Follow these steps to set up your isolated lab environment:

1. **Prepare your Virtual Machine (VM):**
    
    - Create a new Linux VM (e.g., Ubuntu Server, Debian) in VirtualBox or VMware.
    - Allocate sufficient RAM (e.g., 1-2GB) and CPU cores (e.g., 1-2).
    - **Crucially, configure the network adapter for the VM as "Host-Only" or "Internal Network"** to ensure complete isolation. Make a note of the VM's IP address (e.g., `ifconfig` or `ip a`).
    - Install Python 3 and `pip` if they aren't already present (most modern Linux distributions have them).
    
2. **Clone or Copy Lab Files:**

    - Transfer all the lab files (`app.py`, `requirements.txt`, the `templates/` folder, and the `static/` folder) into a directory within your VM (e.g., `/home/youruser/vulnerable_lab`).
    
3. **Install Dependencies:**
    
    - Navigate to the lab directory in your VM's terminal.
    - Install the specific outdated Python packages using `pip`:

```
  cd LAB-6
 pip install -r requirements.txt
```

1. **Run the Vulnerable Flask Application:**
    
        ```
        python3 app.py
        ```
        
    - You should see output indicating that the Flask development server is running, typically on `http://127.0.0.1:5000` or `http://0.0.0.0:5000`.
        
5. **Access the Application:**
    
    - From a web browser _within your VM_, navigate to `http://127.0.0.1:5000`.
    - If you've configured your VM's network to allow host-only access and port forwarding (e.g., 5000 from guest to 5000 on host), you _might_ be able to access it from your host machine's browser at `http://localhost:5000`. **However, for maximum safety, it's recommended to do all interaction from within the VM.**
## **Lab Modules**

Navigate to the links below (or directly in your VM's browser) to start each lab exercise.

### **Module 1: Flask 0.12 - XSS via Host Header**

- **Vulnerability:** Cross-Site Scripting (XSS) via a crafted `Host` header.
    
- **Exploit Example:**
- 
```
curl -H "Host: <script>alert('XSS from Host Header!')</script>" http://127.0.0.1:5000/host_xss
```

- **Lab URL:** `http://127.0.0.1:5000/host_xss`
    
- Check information in the terminal in an alert box
### **Module 2: PyJWT < 1.5.0 - Token Forgery (None Algorithm)**

- **Vulnerability:** JWT token signature bypass by using the "none" algorithm.

- **Exploit Example (Conceptual):**

    ```
    # This is a Python snippet to illustrate how a token with "none" algorithm might be created.
    # You'll use a JWT debugger tool for the actual lab exercise.
    import jwt
    jwt.encode({"user": "admin"}, None, algorithm="none")
    ```

- **Lab URL:** `http://127.0.0.1:5000/jwt_login`

- **Flag:** Will appear on the page if you successfully forge an admin token and the vulnerable server processes it.
### **Module 3: Werkzeug < 0.11.11 - Debugger Remote Code Execution (RCE)**

- **Vulnerability:** Exploiting the Werkzeug debugger pin to gain a remote shell.
- **Conditions:** `debug=True` is enabled in `app.py`.
- **Lab URL:** `http://127.0.0.1:5000/debug_rce`
- **Flag:** You will execute a Python command within the debugger console to reveal information.


##### ⚠️ *The full version of the application is currently under development and will be available soon. Stay tuned!*