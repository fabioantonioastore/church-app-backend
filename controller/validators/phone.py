import re
import phonenumbers
from phonenumbers import NumberParseException
from controller.errors.http.exceptions import bad_request
from typing import NoReturn


class PhoneValidator:
    def __init__(self, phone: str):
        self.phone = phone
        self.is_valid_phone_number()

    def is_valid_phone_number(self) -> NoReturn:
        cleaned_number = re.sub(r"[ \-\(\)]", "", self.phone)
        pattern = re.compile(r"^\+?\d{1,3}\d{6,14}$")
        if not pattern.match(cleaned_number):
            raise bad_request(f"Invalid phone format: {self.phone}")
        try:
            parsed_number = phonenumbers.parse(cleaned_number, None)
            return phonenumbers.is_valid_number(parsed_number)
        except NumberParseException as error:
            raise bad_request(f"This is not a valid number: {error!r}")
