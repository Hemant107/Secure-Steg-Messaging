import base64, os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_bytes_with_password(data, password):
    salt = os.urandom(16)
    key = derive_key(password, salt)
    return salt + Fernet(key).encrypt(data)

def decrypt_bytes_with_password(data, password):
    salt, ciphertext = data[:16], data[16:]
    key = derive_key(password, salt)
    return Fernet(key).decrypt(ciphertext)