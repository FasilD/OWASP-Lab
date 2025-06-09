# OWASP A01:2021 - Broken Access Control Lab

## Overview

Broken Access Control occurs when an application fails to properly enforce restrictions on what authenticated users are allowed to do. This lab demonstrates several real-life access control issues using a deliberately vulnerable Flask web app.
## Lab Features

- User login with session-based access  
- Insecure direct object references (IDOR)  
- Missing function-level access control  
- Unprotected admin panel  
##  Setup Instructions

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
## Scenarios to Explore
##### 1. Insecure Direct Object Reference (IDOR)
- Try accessing /message/2 after logging in as user ID 1 (Alice).
- This simulates unauthorized access to another user's data.
##### 2. Missing Function-Level Access Control
- Any authenticated user can access the /admin panel, no role checks in place.
##### 3. Role Escalation
- Edit your own profile at /edit_profile and change the role from "user" to "admin".
### Learning Objectives
- Understand how broken access controls occur in real apps.
- Identify insecure URL parameters and endpoints.
- Realize the importance of backend role checks, not just frontend UX.
- Learn how attackers escalate privilege or bypass restrictions.