# OWASP A04:2021 - Insecure Design Lab

This lab simulates insecure design vulnerabilities using a realistic Python-based Flask web application called **QuickWallet**. It demonstrates common flaws found in modern web applications where logic is implemented insecurely — a critical risk highlighted in [OWASP Top 10: A04 - Insecure Design](https://owasp.org/Top10/A04_2021-Insecure_Design/).
##  Objectives

This lab aims to help developers and security learners:

- Understand and identify real-world insecure design flaws.
- Practice exploiting logic-based vulnerabilities.
- Think like an attacker to improve secure coding practices.

##  Vulnerabilities Simulated

| Vulnerability                         | Description |
|--------------------------------------|-------------|
| ❌ Insecure Authentication Logic      | No password hashing, plaintext storage |
| ❌ Auto-account creation on login     | No registration control |
| ❌ Admin panel with no access control | Anyone can access `/admin` |
| ❌ Missing input validation           | No balance check, negative transfers possible |
| ❌ Missing authorization on actions   | No role check for sensitive operations |
| ❌ Missing CSRF protection            | No CSRF tokens or session binding |

##  Setup Instructions

###  Requirements

- Python 3.x
- `pip` package manager

###  Installation

#### 1. Clone the repository:

```
   git clone https://github.com/yourusername/owasp-a04-insecure-design-lab.git
   cd owasp-a04-insecure-design-lab
```
#### 2. Install dependencies:

```
pip install flask
```
#### 3. Run the app:

```
python app.py
```
#### 4.Visit the app at:
```
http://127.0.0.1:5000
```

### Walkthrough & Questions (For Learners)
Download the PDF walkthrough (coming soon) which includes:

Step-by-step attack simulation

Screenshot references

Fix recommendations

End-of-lab reflection questions
### Recommended Improvements (Security Hardening)
Use password hashing with bcrypt or werkzeug.security

Implement role-based access control for /admin
Validate transfer inputs (e.g., positive amounts)
Add CSRF protection using Flask-WTF
Separate login and registration
Log user actions for auditing

### License
📄 License This project is licensed under the [MIT License](https://github.com/FasilD/OWASP-Lab/blob/main/LICENSE).
Feel free to fork, modify, and share.

### Author
## Powered By

**QState Cyber Security**  
## Contact

For feedback, suggestions, or issues:  
📧 info@qstatesec.com  
🌐 [qstatesec.com](https://qstatesec.com)