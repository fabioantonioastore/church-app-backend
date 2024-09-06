import firebase_admin
from firebase_admin import credentials
from typing import NoReturn

FIREBASE_CREDENTIALS_PATH = "firebase_credentials.json"


def initialize_firebase() -> NoReturn:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)
