import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import routers.user
import routers.community
import routers.login
import routers.warning
from controller.auth import jwt
from models.community import Community
from controller.crud.community import CommunityCrud
from database.session import session
from controller.crud.user import UserCrud
from models.user import User
from schemas.sign import SignUp
from controller.errors.http.exceptions import internal_server_error, bad_request
from controller.validators.sign_validator import SignUpValidator
from controller.crud.login import LoginCrud
from controller.src.login import create_login

login_crud = LoginCrud()
community_crud = CommunityCrud()
user_crud = UserCrud()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(routers.user.router)
app.include_router(routers.community.router)
app.include_router(routers.login.router)
app.include_router(routers.warning.router)

@app.get("/")
async def root():
    access_token = jwt.create_access_token("hello@gmail.com")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/community/root")
async def create_community():
    a = Community()
    a.id = str(uuid.uuid4())
    a.name = 'community'
    a.email = "a@gmail.com"
    a.image = bytes("asb", 'utf-8')
    a.patron = "hello"
    a.location = "something"

    return await community_crud.create_community(session, a)

@app.post('/council')
async def signup(sign_data: SignUp):
    sign_data = dict(sign_data)
    SignUpValidator(sign_data)
    user = await create_user(sign_data)
    user.position = "council member"
    login = create_login(sign_data)
    login.position = "council member"
    try:
        await user_crud.create_user(session, user)
        try:
            await login_crud.create_login(session, login)
        except:
            await user_crud.delete_user(session, user)
            raise internal_server_error("Database failed to create user")
    except:
        raise bad_request("User already exist")
    return {"access_token": jwt.create_access_token(get_plain_cpf(user.cpf))}

@app.post('/parish')
async def signup(sign_data: SignUp):
    sign_data = dict(sign_data)
    SignUpValidator(sign_data)
    user = await create_user(sign_data)
    user.position = "parish member"
    login = create_login(sign_data)
    login.position = "parish member"
    try:
        await user_crud.create_user(session, user)
        try:
            await login_crud.create_login(session, login)
        except:
            await user_crud.delete_user(session, user)
            raise internal_server_error("Database failed to create user")
    except:
        raise bad_request("User already exist")
    return {"access_token": jwt.create_access_token(get_plain_cpf(user.cpf))}
    