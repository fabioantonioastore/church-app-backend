from controller.errors.cpf_validator_error import CPFValidatorError

class CPFValidator():
    def __init__(self, cpf: str):
        self.cpf = cpf
        self.has_eleven_digits()
        self.verify_first_verificator_digit()
        self.verify_second_verificator_digit()
    def has_eleven_digits(self) -> None:
        if not(len(self.cpf) == 11): raise CPFValidatorError("CPF don't has eleven digits")

    def verify_first_verificator_digit(self) -> None:
        sum = 0
        size = 10
        for i in range(9):
            sum += int(self.cpf[i]) * size
            size -= 1
        digit_one = 11 - (sum % 11)
        if digit_one > 9: digit_one = 0

        if int(self.cpf[9]) != digit_one: raise CPFValidatorError("First verificator digit is wrong")

    def verify_second_verificator_digit(self) -> None:
        sum = 0
        size = 11
        for i in range(10):
            sum += int(self.cpf[i]) * size
            size -= 1
        digit_two = 11 - (sum % 11)
        if digit_two > 9: digit_two = 0

        if int(self.cpf[10]) != digit_two: raise CPFValidatorError("Second verificator digit is wrong")