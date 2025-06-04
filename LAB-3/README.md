OWASP Injection Vulnerability Lab

Welcome to the **OWASP Injection Lab** by **QState Cyber Security**.  
This lab is a hands-on, vulnerable web application built with Flask to help learners and professionals explore and exploit various injection vulnerabilities in a controlled environment.


## Lab Features

This lab simulates real-world injection vulnerabilities based on [OWASP Top 10](https://owasp.org/Top10/):

| Vulnerability Type       | URL Endpoint     | Description                              |
|--------------------------|------------------|------------------------------------------|
| SQL Injection (Login)    | `/login`         | Classic authentication bypass example    |
| SQL Injection (Search)   | `/search`        | Query manipulation on search             |
| Stored SQL Injection     | `/feedback`      | Persistent SQL injection in forms        |
| XPath Injection          | `/lookup`        | Injection targeting XML data             |
| NoSQL Injection          | `/usersearch`    | Exploit non-relational database queries  |
| Command Injection        | `/ping`          | Inject OS commands into user input       |

---

## Getting Started

### Prerequisites
- Python 3.8+
- Flask

### Installation

#### **Clone the repository:**

```
   git clone https://github.com/yourusername/owasp-injection-lab.git
   cd owasp-injection-lab
```
#### **Install dependencies:**
   

```
pip install -r requirements.txt
```

#### **Run the lab:**

```
flask --app app run
or

python3 app.py
```

#### **Initialize/reset the database:**  
```
Visit:
  
http://localhost:5000/initdb
```
## Usage

- Start from the [Login page](http://localhost:5000/login)
- Explore each vulnerability endpoint listed above.
- Try manual attacks (e.g. `' OR 1=1--`) or automated tools (e.g. sqlmap).
- Successfully exploited vulnerabilities will reveal `🏁 Flag` values as proof of concept.
## Disclaimer

> ⚠️ **This lab is for educational and ethical hacking purposes only.** Do NOT deploy it on the internet or use it for malicious purposes.

## Educational Value

This lab is aligned with:

- OWASP Top 10
- CWE Top 25
- Cybersecurity fundamentals for Red Teamers & Pentesters

## Powered By

**QState Cyber Security**  
## Contact

For feedback, suggestions, or issues:  
📧 info@qstatesec.com  
🌐 [qstatesec.com](https://qstatesec.com)