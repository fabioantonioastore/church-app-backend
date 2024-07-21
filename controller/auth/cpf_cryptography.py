from os import getenv
from dotenv import load_dotenv

load_dotenv()
CRYPTO_KEY = getenv('CRYPTO_KEY')

def get_crypted_cpf(cpf: str) -> str:
    encrypted_chars = []
    for i in range(len(cpf)):
        key_c = CRYPTO_KEY[i % len(CRYPTO_KEY)]
        encrypted_c = chr(ord(cpf[i]) ^ ord(key_c))
        encrypted_chars.append(encrypted_c)
    encrypted_data = ''.join(encrypted_chars)
    return encrypted_data

def get_plain_cpf(encrypted_cpf: str) -> str:
    decrypted_chars = []
    for i in range(len(encrypted_cpf)):
        key_c = CRYPTO_KEY[i % len(CRYPTO_KEY)]
        decrypted_c = chr(ord(encrypted_cpf[i]) ^ ord(key_c))
        decrypted_chars.append(decrypted_c)
    decrypted_data = ''.join(decrypted_chars)
    return decrypted_data