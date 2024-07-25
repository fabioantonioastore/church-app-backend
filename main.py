import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import routers.user
import routers.community
import routers.login
from controller.auth import jwt
from models.community import Community
from controller.crud.community import CommunityCrud
from database.session import session
from controller.crud.user import UserCrud

community_crud = CommunityCrud()
user_crud = UserCrud()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(routers.user.router)
app.include_router(routers.community.router)
app.include_router(routers.login.router)

@app.get("/")
async def root():
    access_token = jwt.create_access_token("hello@gmail.com")
    return {"access_token": access_token, "token_type": "bearer"}

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