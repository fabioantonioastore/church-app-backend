from models.number import Number


def create_number_model(user_id: str, number: str) -> Number:
    number_model = Number(
        number=number,
        user_id=user_id
    )
    return number_model
