from fastapi import APIRouter
from schemas.sign import SignIn, SignUp, SignInAdmin
from controller.validators.sign_validator import SignUpValidator
from controller.src.login import create_login, verify_user_login, verify_admin_login
from controller.crud.login import LoginCrud
from database.session import session
from controller.crud.user import UserCrud
from controller.src.user import create_user
from controller.auth import jwt
from controller.errors.crud_error import CrudError

router = APIRouter()
login_crud = LoginCrud()
user_crud = UserCrud()

@router.post("/signin")
async def signin(sign_data: SignIn):
    sign_data = dict(sign_data)
    if await verify_user_login(sign_data):
        return jwt.create_access_token(sign_data['cpf'])
    return "Password or CPF is not correct"

@router.post("/admin/sign")
async def sign_in_admin(sign_data: SignInAdmin):
    sign_data = dict(sign_data)
    if await verify_admin_login(sign_data):
        return jwt.create_access_token(sign_data['cpf'], sign_data['position'])
    return "Password or CPF is not correct"

@router.post("/signup")
async def signup(sign_data: SignUp):
    sign_data = dict(sign_data)
    SignUpValidator(sign_data)
    user = create_user(sign_data)
    login = create_login(sign_data)

    try:
        await user_crud.create_user(session, user)
        try:
            await login_crud.create_login(session, login)
        except CrudError as crud_error:
            await user_crud.delete_user(session, user)
            raise crud_error("Database failed on create user")
    except:
        return "User already exist"

    return jwt.create_access_token(user.cpf)