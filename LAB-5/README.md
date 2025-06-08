# OWASP A05:2021 – Security Misconfiguration Lab


## 1. Introduction

Welcome to the **OWASP A05:2021 – Security Misconfiguration Lab**. This hands-on environment features a intentionally vulnerable Flask web application designed to demonstrate common security misconfigurations that fall under the OWASP Top 10 A05:2021 category.

In this lab, you will act as an ethical hacker, identifying and exploiting various misconfigurations to uncover hidden "flags." Following the exploitation phase, you will then apply the necessary remediations to secure the application, reinforcing your understanding of secure coding practices and defensive measures.

## 2. Learning Objectives

By completing this lab, you will gain practical experience in:

- Understanding the **impact** of common security misconfigurations on web applications.
- Practicing **penetration testing techniques** to discover misconfigured settings and exposed resources.
- Identifying specific vulnerabilities such as **default credentials, verbose errors, sensitive file exposure, and missing security controls**.
- Learning how to **remediate** these vulnerabilities effectively to harden application security.
- Using common command-line tools for web content discovery (e.g., `gobuster`, `ffuf`).

## 3. Vulnerabilities Covered

This lab specifically focuses on the following types of security misconfigurations:

- **Default/Hardcoded Credentials:** Use of easily guessable or default administrative login credentials.
- **Verbose Error Messages:** Application revealing sensitive system information through detailed error messages (e.g., stack traces).
- **Sensitive File Exposure:** Critical configuration files (`config.py`) and application source code (`app.py`) made publicly accessible via direct URL paths.
- **Unnecessary Features / Default Content Exposure:** Default administrative reports or unused features left exposed on the server (e.g., `admins/report.txt`).
- **Missing Security Headers:** Lack of essential HTTP security headers (e.g., `X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`) weakening browser-side protections.
- **Overly Verbose Logging:** Application logging sensitive information (like plaintext passwords) to its console/logs, making it vulnerable if logs are compromised.

## 4. Prerequisites

To run this lab, you will need:

- **Docker Desktop:** If you wish to use Docker make sure Docker is installed and running on your system (Windows, macOS, or Linux).
- **Basic Command Line Knowledge:** Familiarity with navigating directories and running commands in a terminal.
- **(Optional but Recommended for Automated Discovery):** Tools like `gobuster` or `ffuf` if you wish to simulate automated content discovery (commonly found in Kali Linux or Parrot OS).

## 5. Lab Setup

Follow these steps to get the vulnerable lab application up and running:

1. **Clone the Repository (if applicable) or Navigate to the Lab Directory:**
    
    Bash
    
    ```
    cd LAB-5
    ```
    
2. **Ensure Vulnerable Version Configuration:** Before building, ensure the `app.py` file has the "VULNERABLE VERSION" code blocks uncommented and the "SECURE VERSION" blocks commented out. Also, verify that the `/configs/` and `/admins/` directories exist with their respective files (`config.py` and `report.txt`).

3. **Build and Run the Docker Containers:**
   
    ```
    python3 app.py
    or
    docker-compose up --build
    ```
    
    This command will build the Docker image and start the application. It might take a few minutes on the first run.
    
4. **Access the Application:** Once Docker reports that the Flask application is running, open your web browser and navigate to: `http://localhost:5000/`

## 6. How to Use the Lab

Your mission is to:

1. **Identify:** Discover the various security misconfigurations present in the application.
2. **Exploit:** Demonstrate the impact of these misconfigurations by accessing sensitive information or unauthorized areas.
3. **Find Flags:** Each successful exploitation will reveal a hidden "FLAG{...}" string, indicating you've successfully completed that part of the lab.
4. **Remediate:** Once you've found all flags, modify the application's code and configuration to fix the vulnerabilities.

**For detailed instructions, hints, and step-by-step guidance on identifying, exploiting, and remediating each vulnerability, please refer to the `testing-guide.md` file located in the lab's root directory.**

### Key Endpoints to Explore:

- **Login Page:** `http://localhost:5000/login`
- **Broken Page (for testing errors):** `http://localhost:5000/broken`
- **For other sensitive endpoints, you'll need to discover them!**

## 7. Lab Structure Overview

The core components of this lab include:

- `app/`: Contains the Flask application code.
    - `app.py`: The main Flask application with both vulnerable and secure code sections.
    - `templates/`: HTML templates for the web pages.
    - `static/`: Static assets like CSS and images.
    - `configs/`: Directory containing `config.py` (exposed vulnerable config).
    - `admins/`: Directory containing `report.txt` (exposed unnecessary file).
- `docker-compose.yml`: Defines the Docker services for the lab.
- `Dockerfile`: Instructions for building the Flask application's Docker image.
- `testing-guide.md`: **Your primary guide for the lab**, containing detailed instructions, hints, exploitation steps, and remediation guidance for each vulnerability.

## 8. Credits

This lab was developed by **QState Cyber Security** to provide practical training on web application security.

## 9. Disclaimer

This lab is created for **educational and ethical hacking purposes only**. Do not use the techniques or information learned from this lab on any systems without explicit permission from the owner. Unauthorized access to computer systems is illegal and punishable by law. The creators and distributors of this lab are not responsible for any misuse or damage caused by its use.