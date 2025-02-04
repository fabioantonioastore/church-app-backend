from controller.validators.sign_validator import SignUpValidator


class TestSign:
    def __init__(self):
        pass

    def sign_up(self, sign_up_data: dict) -> bool:
        try:
            SignUpValidator(sign_up_data)
            return True
        except:
            return False

    def sign_in(self, sign_in_data: dict) -> bool:
        pass
