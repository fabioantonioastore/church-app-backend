from controller.auth.twillio import client, TWILIO_NUMBER
from random import randint


def send_message(destination_number: str, message: str) -> None:
    client.messages.create(body=message, to=destination_number, from_=TWILIO_NUMBER)


def generate_verification_code() -> int:
    VERIFICATION_CODE_SIZE = 4
    code = ""
    for _ in range(VERIFICATION_CODE_SIZE):
        code += str(randint(0, 9))
    return int(code)
