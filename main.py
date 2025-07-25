import datetime
import uuid

from sqlalchemy.util import await_only

from controller.auth.firebase import initialize_firebase
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import router.user
import router.community
import router.login
import router.warning
import router.dizimo_payment
import router.web.web_push_notification
import router.image
import router.sms
import router.finance
import router.clean
from controller.auth import jwt
from controller.src.pix_payment import (
    make_post_pix_request,
    create_customer,
    PixPayment,
)
from asyncio import run
from models.community import Community
from controller.crud.community import CommunityCrud
from controller.crud.user import UserCrud
from models.user import User
from schemas.sign import SignUp
from controller.errors.http.exceptions import (
    internal_server_error,
    bad_request,
)
from controller.validators.sign_validator import SignUpValidator
from controller.crud.login import LoginCrud
from controller.src.login import create_login
from controller.src.user import create_user
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from apscheduler.triggers.cron import CronTrigger
from controller.jobs.dizimo_payment import (
    create_month_dizimo_payment_and_transfer_payments_values,
)
from controller.crud.dizimo_payment import DizimoPaymentCrud
from router.middleware.authorization import verify_user_access_token
from controller.src.dizimo_payment import (
    is_valid_payment_status,
    test_create_dizimo_payment,
    complete_dizimo_payment,
)
from controller.src.web_push_notification import (
    initiciate_push_notification_jobs,
)
from controller.crud.web_push import WebPushCrud
from apscheduler.triggers.date import DateTrigger
from controller.jobs.web_push_notification import execute_notification
from controller.jobs.finance import calc_community_available_money
from controller.jobs.dizimo_payment import set_dizimo_payments_expired
from controller.jobs.clean import create_new_cleaning
from controller.crud.clean import CleanCRUD

login_crud = LoginCrud()
community_crud = CommunityCrud()
user_crud = UserCrud()
dizimo_payment_crud = DizimoPaymentCrud()
scheduler = AsyncIOScheduler()
web_push_crud = WebPushCrud()
clean_crud = CleanCRUD()


@asynccontextmanager
async def event_manager(app: FastAPI):
    try:
        initialize_firebase()
        scheduler.start()
        initiciate_push_notification_jobs(scheduler)
        scheduler.add_job(
            create_month_dizimo_payment_and_transfer_payments_values,
            trigger=CronTrigger(day=1, hour=0, minute=0, second=0),
        )
        scheduler.add_job(
            calc_community_available_money,
            trigger=CronTrigger(day=1, hour=0, minute=0, second=0),
        )
        scheduler.add_job(
            set_dizimo_payments_expired,
            trigger=CronTrigger(day="last", hour=23, minute=59),
        )
        scheduler.add_job(
            create_new_cleaning, trigger=CronTrigger(day=1, hour=0, minute=0, second=0)
        )
        yield
    finally:
        scheduler.shutdown()


app = FastAPI(lifespan=event_manager)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router.user.router)
app.include_router(router.community.router)
app.include_router(router.login.router)
app.include_router(router.warning.router)
app.include_router(router.dizimo_payment.router)
app.include_router(router.web.web_push_notification.router)
app.include_router(router.image.router)
app.include_router(router.sms.router)
app.include_router(router.finance.router)
app.include_router(router.clean.router)


@app.get("/dizimo/get_all")
async def get_all_dizimo():
    return await dizimo_payment_crud.get_all()


@app.get("/clean/get_all")
async def get_all_clean():
    return await clean_crud.get_all()


@app.get("/communities")
async def get_all():
    return await community_crud.get_all_communities()


@app.get("/abcd")
async def get_all_pay():
    return await dizimo_payment_crud.get_all()


@app.post("/community/root")
async def create_community():
    a = Community()
    a.id = str(uuid.uuid4())
    a.name = "community"
    a.email = "a@gmail.com"
    a.image = None
    a.patron = "hello"
    a.location = "something"

    return await community_crud.create_community(a)


@app.post("/council")
async def signup(sign_data: SignUp):
    sign_data = dict(sign_data)
    SignUpValidator(sign_data)
    user = await create_user(sign_data)
    user.position = "council member"
    login = create_login(sign_data)
    login.position = "council member"
    try:
        await user_crud.create_user(user)
        try:
            await login_crud.create_login(login)
        except:
            await user_crud.delete_user(user)
            raise internal_server_error("Database failed to create user")
    except:
        raise bad_request("User already exist")
    return {
        "access_token": jwt.create_access_token(user.cpf, position="council member")
    }


@app.post("/parish")
async def signup(sign_data: SignUp):
    sign_data = dict(sign_data)
    SignUpValidator(sign_data)
    user = await create_user(sign_data)
    user.position = "parish leader"
    login = create_login(sign_data)
    login.position = "parish leader"
    try:
        await user_crud.create_user(user)
        try:
            await login_crud.create_login(login)
        except:
            await user_crud.delete_user(user)
            raise internal_server_error("Database failed to create user")
    except:
        raise bad_request("User already exist")
    return {"access_token": jwt.create_access_token(user.cpf, position="parish leader")}


@app.patch(
    "/make_payment/{year}/{month}/{status}",
    dependencies=[Depends(verify_user_access_token)],
)
async def make_payment(
    year: int,
    month: str,
    status: str,
    user: dict = Depends(verify_user_access_token),
):
    if not (is_valid_payment_status(status)):
        raise "Invalid status: active, paid, expired"
    user = await user_crud.get_user_by_cpf(user["cpf"])
    dizimo = await dizimo_payment_crud.get_payment_by_month_year_and_user_id(
        month, int(year), user.id
    )
    await dizimo_payment_crud.update_status(dizimo.id, status)
    return "Ok"


@app.post(
    "/create/dizimo_payment/{year}/{month}",
    dependencies=[Depends(verify_user_access_token)],
)
async def create_payment_router(
    year: int, month: str, user: dict = Depends(verify_user_access_token)
):
    user = await user_crud.get_user_by_cpf(user["cpf"])
    dizimo = await test_create_dizimo_payment(user, int(year), month)
    community = await community_crud.get_community_by_id(user.community_id)
    pix_payment = PixPayment(
        value=10,
        customer=create_customer(user),
        correlationID=str(uuid.uuid4()),
        subaccount=community.pix_key
    )
    pix_payment = make_post_pix_request(pix_payment)
    dizimo = complete_dizimo_payment(dizimo, pix_payment)
    return await dizimo_payment_crud.create_payment(dizimo)


@app.delete(
    "/delete/dizimo_payment/{year}/{month}",
    dependencies=[Depends(verify_user_access_token)],
)
async def delete_payment_router(
    year: int, month: str, user: dict = Depends(verify_user_access_token)
):
    user = await user_crud.get_user_by_cpf(user["cpf"])
    dizimo = await dizimo_payment_crud.get_payment_by_month_year_and_user_id(
        month, int(year), user.id
    )
    await dizimo_payment_crud.delete_payment_by_id(dizimo.id)
    return "Deleted"


@app.get("/abcde")
async def a():
    return await web_push_crud.get_all_tokens()


@app.get("/test/message/{token}")
async def test_async_message(token: str):
    scheduler.add_job(
        execute_notification,
        trigger=DateTrigger(datetime.datetime.now()),
        args=[token, "hello", "hello"],
    )
    for i in range(1, 5):
        TIME = datetime.datetime.now() + datetime.timedelta(minutes=i)
        scheduler.add_job(
            execute_notification,
            trigger=DateTrigger(TIME),
            args=[token, "hello", "hello"],
        )
    return "Ok"


async def main():
    await create_new_cleaning()


if __name__ == "__main__":
    run(main())
