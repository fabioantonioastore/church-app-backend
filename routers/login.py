from fastapi import APIRouter, status
from schemas.sign import SignIn, SignUp, SignInAdmin
from controller.validators.sign_validator import SignUpValidator
from controller.src.login import create_login, verify_user_login, verify_admin_login
from controller.crud.login import LoginCrud
from database.session import session
from controller.crud.user import UserCrud
from controller.src.user import create_user
from controller.auth import jwt
from controller.errors.http.exceptions import internal_server_error, bad_request

router = APIRouter()
login_crud = LoginCrud()
user_crud = UserCrud()

@router.post("/signin", status_code=status.HTTP_200_OK)
async def signin(sign_data: SignIn):
    sign_data = dict(sign_data)
    if await verify_user_login(sign_data):
        return {"access_token": jwt.create_access_token(sign_data['cpf'])}
    return bad_request("Password or CPF is not correct")

@router.post("/admin/sign", status_code=status.HTTP_200_OK)
async def sign_in_admin(sign_data: SignInAdmin):
    sign_data = dict(sign_data)
    if await verify_admin_login(sign_data):
        return {"access_token": jwt.create_access_token(sign_data['cpf'], sign_data['position'])}
    return bad_request("Password or CPF is not correct")

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(sign_data: SignUp):
    sign_data = dict(sign_data)
    SignUpValidator(sign_data)
    user = await create_user(sign_data)
    login = create_login(sign_data)
    try:
        await user_crud.create_user(session, user)
        try:
            await login_crud.create_login(session, login)
        except:
            await user_crud.delete_user(session, user)
            raise internal_server_error("Database failed to create user")
    except:
        raise bad_request("User already exist")

    return {"access_token": jwt.create_access_token(user.cpf)}