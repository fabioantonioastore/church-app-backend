import firebase_admin
from firebase_admin import credentials
from typing import NoReturn


def initialize_firebase() -> NoReturn:
    cred = credentials.Certificate()
    firebase_admin.initialize_app(cred)
