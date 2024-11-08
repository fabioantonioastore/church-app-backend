from fastapi import APIRouter, status
from controller.crud import NumberCrud, LoginCrud, UserCrud
from controller.src.sms import generate_verification_code, send_message
from controller.errors.http.exceptions import not_acceptable

router = APIRouter()
number_crud = NumberCrud()
login_crud = LoginCrud()
user_crud = UserCrud()


@router.get('/password_recovery/{number}', status_code=status.HTTP_204_NO_CONTENT)
async def get_password_recovery_code(number: str):
    code = generate_verification_code()
    await number_crud.update_verification_code(number, code)
    message = f"Your recovery code is: {code}"
    send_message(number, message)


@router.get('/password_recovery/{number}/{code}', status_code=status.HTTP_200_OK)
async def verify_recovery_code(number: str, code: int):
    DEFAULT_PASSWORD = "Re1234@@"
    number_model = await number_crud.get_number_model_by_number(number)
    if number_model.verification_code:
        if number_model.verification_code == code:
            user = await user_crud.get_user_by_id(number_model.user_id)
            await login_crud.update_password(user.cpf, DEFAULT_PASSWORD)
            return {"new_password": DEFAULT_PASSWORD}
    raise not_acceptable(f"Invalid code")
