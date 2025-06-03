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
