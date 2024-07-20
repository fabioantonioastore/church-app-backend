import re
from controller.errors.password_error import PasswordError

class PasswordValidator():
    def __init__(self, password: str):
        self.password = password
        self.has_minimium_characters()
        self.has_space()
        self.has_upper_letter()
        self.has_number()
        self.has_special_character()

    def has_minimium_characters(self):
        if len(self.password) < 8: raise PasswordError("Password have to have a minimium of 8 characteres")
    def has_space(self):
        if " " in self.password: raise PasswordError("Password cannot have space")

    def has_upper_letter(self) -> None:
        if not(re.search(r'[A-Z]', self.password)): raise PasswordError("Password don't have upper case letter")

    def has_special_character(self) -> None:
        if not(re.search(r'[!@#$%^&*(),.?":|<>;]', self.password)): raise PasswordError("Password don't have special caracter")

    def has_number(self) -> None:
        if not(re.search(r'[0-9]', self.password)): raise PasswordError("Password don't have a number")