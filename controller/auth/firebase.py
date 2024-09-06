import firebase_admin
from firebase_admin import credentials
from typing import NoReturn

FIREBASE_CONFIG = "firebase_credentials.json"


def initialize_firebase() -> NoReturn:
    cred = credentials.Certificate(FIREBASE_CONFIG)
    firebase_admin.initialize_app(cred)
