import re
from controller.errors.name_error import NameError

class NameValidator:
    def __init__(self, name: str):
        self.name = name
        self.has_number()
        self.has_special_character()
        self.is_sort_name()

    def has_number(self) -> None:
        if re.search(r'[0-9]', self.name): raise NameError("Invalid name, name has number")

    def has_special_character(self) -> None:
        if re.search(r'[!@#$%^&*(),.?|<>";]', self.name): raise NameError("Invalid name, name has special character")

    def is_sort_name(self) -> None:
        if len(self.name) < 3: raise NameError("This name is too short to be a name")