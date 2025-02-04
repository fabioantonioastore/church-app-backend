from controller.validators.cpf import CPFValidator
from controller.validators.date import DateValidator
from controller.validators.password import PasswordValidator
from controller.validators.name import NameValidator
from controller.validators.phone import PhoneValidator


class SignUpValidator:
    def __init__(self, data: dict):
        CPFValidator(data["cpf"])
        NameValidator(data["name"])
        DateValidator(data["birthday"])
        PasswordValidator(data["password"])
        PhoneValidator(data["phone"])


class SignInValidator:
    def __int__(self, data: dict):
        CPFValidator(data["cpf"])
        PasswordValidator(data["password"])
