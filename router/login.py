from fastapi import APIRouter, status
from schemas.sign import SignIn, SignUp
from controller.validators.sign_validator import SignUpValidator
from controller.src.login import create_login, verify_user_login
from controller.crud import LoginCrud
from controller.crud import UserCrud
from controller.src.user import create_user
from controller.src.number import create_number_model
from controller.auth import jwt
from controller.errors.http.exceptions import internal_server_error, bad_request
from controller.src.user import convert_user_to_dict
from controller.src.dizimo_payment import create_dizimo_payment
from controller.crud import DizimoPaymentCrud, NumberCrud

router = APIRouter()
login_crud = LoginCrud()
user_crud = UserCrud()
dizimo_payment_crud = DizimoPaymentCrud()
number_crud = NumberCrud()


@router.post("/signin", status_code=status.HTTP_200_OK, summary="Login", description="Do Sign In")
async def signin(sign_data: SignIn):
    sign_data = dict(sign_data)
    if await verify_user_login(sign_data):
        user = await user_crud.get_user_by_cpf(sign_data['cpf'])
        if not (user.active):
            user.active = True
            user = convert_user_to_dict(user)
            await user_crud.update_user(user)
        return {"access_token": jwt.create_access_token(sign_data['cpf'], user.position)}
    return bad_request("Password or CPF is not correct")


@router.post("/signup", status_code=status.HTTP_201_CREATED, summary="Login", description="Create user account")
async def signup(sign_data: SignUp):
    sign_data = dict(sign_data)
    SignUpValidator(sign_data)
    user = await create_user(sign_data)
    login = create_login(sign_data)
    try:
        await user_crud.create_user(user)
        try:
            await login_crud.create_login(login)
        except Exception as error:
            await user_crud.delete_user(user)
            raise internal_server_error(f"Database failed to create user: {error!r}")
    except Exception as error:
        raise bad_request(f"User already exist: {error!r}")
    dizimo_payment = await create_dizimo_payment(user)
    await dizimo_payment_crud.create_payment(dizimo_payment)
    number_model = create_number_model(user.id, user.phone)
    await number_crud.create_number(number_model)
    return {"access_token": jwt.create_access_token(user.cpf)}
