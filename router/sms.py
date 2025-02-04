from fastapi import APIRouter, status
from controller.crud import NumberCrud, LoginCrud, UserCrud
from controller.src.sms import generate_verification_code, send_message
from controller.errors.http.exceptions import not_acceptable

router = APIRouter()
number_crud = NumberCrud()
login_crud = LoginCrud()
user_crud = UserCrud()


@router.get("/password_recovery/{cpf}", status_code=status.HTTP_200_OK)
async def get_password_recovery_code(cpf: str):
    user = await user_crud.get_user_by_cpf(cpf)
    code = generate_verification_code()
    await number_crud.update_verification_code(user.phone, code)
    message = f"Your recovery code is: {code}"
    send_message(user.phone, message)
    return {"phone": user.phone}


@router.get("/password_recovery/{cpf}/{code}", status_code=status.HTTP_200_OK)
async def verify_recovery_code(cpf: str, code: int):
    DEFAULT_PASSWORD = "Re1234@@"
    user = await user_crud.get_user_by_cpf(cpf)
    number_model = await number_crud.get_number_model_by_number(user.phone)
    if number_model.verification_code:
        if number_model.verification_code == code:
            await login_crud.update_password(user.cpf, DEFAULT_PASSWORD)
            return {"new_password": DEFAULT_PASSWORD}
    raise not_acceptable(f"Invalid code")
