from fastapi import APIRouter, status
from schemas.sign import SignIn, SignUp, SignInAdmin
from controller.validators.sign_validator import SignUpValidator
from controller.src.login import create_login, verify_user_login, verify_admin_login
from controller.crud.login import LoginCrud
from database.session import session
from controller.crud.user import UserCrud
from controller.src.user import create_user
from controller.auth import jwt
from controller.errors.http.exceptions import internal_server_error, bad_request, not_acceptable
from controller.src.user import convert_user_to_dict

router = APIRouter()
login_crud = LoginCrud()
user_crud = UserCrud()

@router.post("/signin", status_code=status.HTTP_200_OK, summary="Login", description="Do Sign In")
async def signin(sign_data: SignIn):
    sign_data = dict(sign_data)
    if await verify_user_login(sign_data):
        user = await user_crud.get_user_by_cpf(session, sign_data['cpf'])
        if not(user.active):
            user.active = True
            user = convert_user_to_dict(user)
            await user_crud.update_user(session, user)
        return {"access_token": jwt.create_access_token(sign_data['cpf'], user.position)}
    return bad_request("Password or CPF is not correct")

@router.post("/signup", status_code=status.HTTP_201_CREATED, summary="Login", description="Create user account")
async def signup(sign_data: SignUp):
    sign_data = dict(sign_data)
    SignUpValidator(sign_data)
    user = await create_user(sign_data)
    login = create_login(sign_data)
    try:
        await user_crud.create_user(session, user)
        try:
            await login_crud.create_login(session, login)
        except Exception as error:
            await user_crud.delete_user(session, user)
            raise internal_server_error(f"Database failed to create user: {error!r}")
    except Exception as error:
        raise bad_request(f"User already exist: {error!r}")
    return {"access_token": jwt.create_access_token(user.cpf)}