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
