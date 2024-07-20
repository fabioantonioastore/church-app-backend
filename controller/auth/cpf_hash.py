from os import getenv
from dotenv import load_dotenv
from hashlib import sha512

load_dotenv()
CPF_SALT = getenv('CPF_SALT')

def hash_cpf(cpf: str) -> str:
    return sha512((cpf + CPF_SALT).encode('utf-8')).hexdigest()

def verify_cpf_hash(plain_cpf: str, hashed_cpf: str) -> bool:
    return hash_cpf(plain_cpf) == hashed_cpf