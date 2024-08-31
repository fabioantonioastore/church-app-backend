import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import routers.user
import routers.community
import routers.login
import routers.warning
import routers.dizimo_payment
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
from controller.src.user import create_user
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from apscheduler.triggers.cron import CronTrigger
from controller.jobs.dizimo_payment import create_month_dizimo_payment

login_crud = LoginCrud()
community_crud = CommunityCrud()
user_crud = UserCrud()
scheduler = AsyncIOScheduler()

scheduler.add_job(create_month_dizimo_payment, trigger=CronTrigger(day=1, hour=0, minute=0))

@asynccontextmanager
async def event_manager(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=event_manager)

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
app.include_router(routers.dizimo_payment.router)

@app.get('/communities')
async def get_all():
    return await community_crud.get_all_communities(session)

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
    return {"access_token": jwt.create_access_token(user.cpf, position='council member')}

@app.post('/parish')
async def signup(sign_data: SignUp):
    sign_data = dict(sign_data)
    SignUpValidator(sign_data)
    user = await create_user(sign_data)
    user.position = "parish leader"
    login = create_login(sign_data)
    login.position = "parish leader"
    try:
        await user_crud.create_user(session, user)
        try:
            await login_crud.create_login(session, login)
        except:
            await user_crud.delete_user(session, user)
            raise internal_server_error("Database failed to create user")
    except:
        raise bad_request("User already exist")
    return {"access_token": jwt.create_access_token(user.cpf, position='parish leader')}
    