import uuid

from fastapi import FastAPI, Request
import routers.user
import routers.community
import routers.login
from controller.auth import jwt
from schemas.sign import SignIn
from models.community import Community
from controller.crud.community import CommunityCrud
from database.session import session
from controller.crud.user import UserCrud
from controller.auth.cpf_hash import hash_cpf

community_crud = CommunityCrud()
user_crud = UserCrud()

app = FastAPI()

app.include_router(routers.user.router)
app.include_router(routers.community.router)
app.include_router(routers.login.router)

@app.get("/")
async def root():
    access_token = jwt.create_access_token("hello@gmail.com")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/token")
async def token_route(a: SignIn, request: Request):
    return jwt.decode_token(request.headers.get('Authorization'))

@app.post("/community")
async def create_community():
    a = Community()
    a.id = str(uuid.uuid4())
    a.name = 'community'
    a.email = "a@gmail.com"
    a.image = bytes("asb", 'utf-8')
    a.patron = "hello"
    a.location = "something"

    return await community_crud.create_community(session, a)

@app.get("/users")
async def get_all_users():
    return await user_crud.get_user_by_cpf(session, hash_cpf("13184791777"))
