import base64
import hashlib
from cryptography.fernet import Fernet, InvalidToken
from stego import encode_bytes_into_image, decode_bytes_from_image

def generate_key(password):
    key = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(key)

def encrypt_message(message, password):
    key = generate_key(password)
    f = Fernet(key)
    return f.encrypt(message.encode("utf-8"))

def decrypt_message(encrypted_message, password):
    key = generate_key(password)
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode("utf-8")

def encode_image(image_path, message, password, output_path):
    encrypted = encrypt_message(message, password)
    return encode_bytes_into_image(image_path, encrypted, output_path)

def decode_image(image_path, password):
    encrypted_bytes = decode_bytes_from_image(image_path)
    try:
        return decrypt_message(encrypted_bytes, password)
    except InvalidToken:
        return None