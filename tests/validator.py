from controller import validators

class TestValidator:
    def __int__(self):
        pass

    def test_cpf(self, cpf: str) -> bool:
        try:
            validators.cpf.CPFValidator(cpf)
            return True
        except: return False

    def test_password(self, password: str) -> bool:
        try:
            validators.password.PasswordValidator(password)
            return True
        except: return False

    def test_name(self, name: str) -> bool:
        try:
            validators.name.NameValidator(name)
            return True
        except: return False

    def test_birthday(self, birthday: str) -> bool:
        try:
            validators.date.DateValidator(birthday)
            return True
        except: return False