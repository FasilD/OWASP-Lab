# OWASP-Lab
# OWASP Top 10 Hands-On Vulnerability Labs

Welcome to the **OWASP Top 10 Hands-On Labs**,  a fully open-source, developer-friendly project that lets you **exploit**, **understand**, and **fix** real-world web vulnerabilities from the ground up.

- Learn how each OWASP Top 10 risk is introduced in code  
- Exploit each vulnerability with real-world attack techniques  
- Patch and secure the code to learn secure development practices

## Why This Lab Series?

Many platforms like TryHackMe and Hack The Box offer vulnerable applications to *exploit*, but they often **don’t let you recreate or fix** the vulnerabilities.

This lab series changes that.

- Designed for developers, red teamers, students, and trainers  
- Recreate vulnerabilities with real code  
- Test multiple variations of each vulnerability (stored, reflected, authenticated, etc.)  
- Learn how to secure your applications **by fixing the code yourself**  
- Everything runs locally in Docker, easy to spin up and break down


## Included Labs

This project contains one complete lab for each OWASP Top 10 risk:

| #   | OWASP Risk                               | Description                                      |
| --- | ---------------------------------------- | ------------------------------------------------ |
| A01 | Broken Access Control                    | Role bypass, IDOR, method-based control flaws    |
| A02 | Cryptographic Failures                   | Insecure TLS, weak hashing, token leakage        |
| A03 | Injection                                | SQL, Command, and NoSQL injection                |
| A04 | Insecure Design                          | Business logic abuse, insecure flows             |
| A05 | Security Misconfiguration                | Directory listing, verbose errors, default creds |
| A06 | Vulnerable & Outdated Components         | Dependency-based exploits                        |
| A07 | Identification & Authentication Failures | Weak auth, brute-force, session flaws            |
| A08 | Software & Data Integrity Failures       | CI/CD poisoning, insecure deserialization        |
| A09 | Security Logging & Monitoring Failures   | Lack of alerting and log injection               |
| A10 | Server-Side Request Forgery (SSRF)       | Internal resource access and metadata theft      |

> *More advanced and language-specific variants coming soon!*

## How to Use

### 1. Clone the Repository

```
git clone https://github.com/FasilD/OWASP-Lab.git
cd owasp-top10-labs
```
### 2. Launch a Lab
Each lab is Dockerized and self-contained, or you can run the app directly using Python
```
cd LAB-1
python3 app.py
Access the lab at http://127.0.0.1:5000 or whatever port is specified.
```

### 3. Start Practicing
- Follow the README.md inside each lab folder
- Exploit the vulnerability manually or with tools
- Then modify the code to fix the issue (step-by-step guidance included)

### 4. Who Is This For?
- Developers - Learn how security flaws are created in code
- Red Teamers - Simulate real-world attack chains
- Students - Practice hands-on secure coding and exploitation
- Trainers - Use this for teaching secure web development
### 5. Additional Resources

[OWASP Official Site](https://owasp.org/www-project-top-ten/)

### 6. Contributing
Got an idea for a new vulnerability or want to add Python/Java/PHP variants?
Pull requests are welcome! Check out CONTRIBUTING.md for setup instructions.

### Spread the Word
If you find this project helpful:

⭐ Star the repo
🐦 Share it on Twitter or LinkedIn
🎥 Use it in your cybersecurity training or YouTube demos

📄 License
This project is licensed under the MIT License.

Built with ❤️ by the QState Cyber community, to teach, test, and secure the web.
