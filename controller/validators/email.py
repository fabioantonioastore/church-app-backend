import re
from controller.errors.http.exceptions import bad_request

class EmailValidator:
    def __init__(self, email: str):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not(re.match(pattern, email)):
            raise bad_request("It's not a valid email")