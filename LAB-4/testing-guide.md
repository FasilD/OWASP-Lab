# OWASP A04:2021 Insecure Design Lab - Testing Guide

This lab simulates **real-world insecure design flaws** in a modern Flask web application (QuickWallet). Below are the guided test cases to discover and exploit logic issues that align with OWASP A04 vulnerabilities.

##  Pre-requisites

- Python 3.x and pip installed
- Flask environment set up
- Clone and run:
 
```
pip install flask 
python3 lab.py
```

- Navigate to: `http://localhost:5000/`

## Test Case 1: Insecure User Registration Logic

###  What to Test:

- Does the app allow any username/password combo?
- Are passwords stored securely?
### Steps:

1. Go to `/login`
2. Enter a new username and password
3. You’ll be registered silently — no verification or password policies
4. Check `data/users.json` — you’ll see plaintext passwords
### Expected Vulnerability:

- No secure password handling (hashing/salting)
- Insecure default registration logic

## Test Case 2: Logic Flaw in Money Transfer

### What to Test:

- Can a user transfer more money than they have?
- Can you transfer to a fake/non-existent user?

### Steps:

1. Login as `alice / anypass`
2. Go to `/transfer`
3. Send **$10,000** to `bob`
4. Try sending **negative values** or to a new user like `hacker`
###  Expected Vulnerability:

- No balance check
- No input validation
- Automatically creates fake users on-the-fly
## Test Case 3: Admin Access Without Authorization

### What to Test:

- Is the `/admin` route protected?
- Can a normal user access it?
###  Steps:

1. Login as any user
2. Manually navigate to `/admin`
###  Expected Vulnerability:

- No authentication or role check
- All users can access privileged route
## Test Case 4: Broken Authentication

### What to Test:

- Can users login with wrong credentials?
- Are sessions properly handled?
###  Steps:

1. Try logging in with incorrect password for existing user
2. Refresh the page after logout
###  Expected Vulnerability:

- No rate-limiting, lockout, or secure session management
- No logout confirmation
##  Test Case 5: Business Logic Manipulation

### What to Test:

- Can you game the system via UI or hidden inputs?
### Steps:

1. Use DevTools to modify form inputs (e.g., enter script tags, large amounts)
2. Send large transfers multiple times
###  Expected Vulnerability:

- No client/server-side logic protection
- No CSRF tokens or form validation
## Test Case 6: Session Fixation / Hijacking Simulation

### What to Test:

- Can you access dashboard after manual session creation?
### Steps:

#### 1. In browser DevTools, manually inject:

```
document.cookie = "session=spoofedvalue";
```
#### 2. Reload `/dashboard`

### Expected Vulnerability:

- No protection against session hijacking
- No secure flags or expiry for sessions
## Test Case 7: Data Exposure

### What to Test:

- Is sensitive data stored or exposed?
###  Steps:

1. Inspect `data/users.json`
2. Try reading directly if exposed via file path

### Expected Vulnerability:

- Plaintext user passwords
- Local file disclosure if misconfigured
## Bonus: Exploit Scenario

**Escalation from user to admin (Generic Flaw)**  
If admin logic depends on username or input control, try creating a user with name `admin`, or manually edit the `users.json` to set `"is_admin": true` and access `/admin`.

##  Summary of Vulnerabilities Simulated

|Vulnerability|Description|
|---|---|
|Insecure Design (A04)|Poorly designed flows with insecure defaults|
|Insecure Authentication|No hashing, easy bypass|
|Broken Access Control|Admin route lacks authorization|
|Business Logic Vulnerabilities|No validation on transfers|
|Insecure Session Management|Session tampering possible|
|Data Exposure|Plaintext storage of sensitive info|
## Tips for Mitigation (For Developers)

- Use strong authentication (hash passwords, validate inputs)
- Implement authorization checks on all sensitive routes
- Sanitize inputs and enforce transfer rules
- Add CSRF protection
- Avoid storing sensitive data in plaintext