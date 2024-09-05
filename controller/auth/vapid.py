from dotenv import load_dotenv
from os import getenv

load_dotenv()

VAPID_PRIVATE_KEY = getenv("VAPID_PRIVATE_KEY")
VAPID_PUBLIC_KEY = getenv("VAPID_PUBLIC_KEY")
VAPID_EMAIL = getenv("VAPID_EMAIL")
VAPID_CLAIMS = {
    "sub": f"mailto:{VAPID_EMAIL}"
}
