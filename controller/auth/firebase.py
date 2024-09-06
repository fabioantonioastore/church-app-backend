import firebase_admin
from firebase_admin import credentials

FIREBASE_CREDENTIALS_PATH = "firebase_credentials.json"


def initialize_firebase():
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)
