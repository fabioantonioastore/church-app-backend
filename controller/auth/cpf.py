from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import os
from dotenv import load_dotenv

load_dotenv()
CRYPTO_KEY = os.getenv("CRYPTO_KEY")


def derive_key(password: str, salt: bytes) -> bytes:
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    return kdf.derive(password.encode())


def encrypt(message: str, password: str = CRYPTO_KEY) -> str:
    salt = os.urandom(16)
    key = derive_key(password, salt)
    nonce = os.urandom(12)
    cipher = Cipher(
        algorithms.AES(key), modes.GCM(nonce), backend=default_backend()
    )
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_message = padder.update(message.encode()) + padder.finalize()

    encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
    encrypted_data = salt + nonce + encryptor.tag + encrypted_message
    return base64.b64encode(encrypted_data).decode("utf-8")


def decrypt(encrypted_message: str, password: str = CRYPTO_KEY) -> str:
    encrypted_data = base64.b64decode(encrypted_message)
    salt, nonce, tag, encrypted_message = (
        encrypted_data[:16],
        encrypted_data[16:28],
        encrypted_data[28:44],
        encrypted_data[44:],
    )
    key = derive_key(password, salt)
    cipher = Cipher(
        algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend()
    )
    decryptor = cipher.decryptor()

    padded_message = decryptor.update(encrypted_message) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_message = unpadder.update(padded_message) + unpadder.finalize()

    return decrypted_message.decode("utf-8")
