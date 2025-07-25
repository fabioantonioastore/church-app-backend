import json
from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from controller.crud import DizimoPaymentCrud, CommunityCrud
from router.middleware.authorization import verify_user_access_token
from controller.crud import UserCrud
from uuid import uuid4
from controller.src.dizimo_payment import (
    dizimo_payment_is_paid,
    complete_dizimo_payment,
    dizimo_payment_is_expired,
)
from controller.errors.http.exceptions import bad_request, not_acceptable
from controller.src.pix_payment import (
    PixPayment,
    PixInfo,
    create_customer,
    make_post_pix_request,
    get_pix_no_sensitive_data,
    get_pix_payment_from_correlation_id,
    is_pix_active,
)
from schemas.dizimo_payment import CreateDizimoPaymentModel
from apscheduler.triggers.date import DateTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from controller.jobs.dizimo_payment import update_payment_and_push_notification
from datetime import datetime, timedelta
from controller.src.dizimo_payment import get_dizimo_payment_no_sensitive_data
from controller.jobs.dizimo_payment import pix_notification_message

router = APIRouter()
dizimo_payment_crud = DizimoPaymentCrud()
user_crud = UserCrud()
community_crud = CommunityCrud()
scheduler = AsyncIOScheduler()


@router.post(
    "/dizimo_payment",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_user_access_token)],
)
async def create_dizimo_payment_router(
    pix_data: CreateDizimoPaymentModel,
    user: dict = Depends(verify_user_access_token),
):
    try:
        scheduler.start()
    except Exception as error:
        pass
    user = await user_crud.get_user_by_cpf(user["cpf"])
    community = await community_crud.get_community_by_id(user.community_id)
    pix_data = dict(pix_data)
    if pix_data["value"] < 1:
        raise bad_request("Value must be greater or equal than 1")
    pix_data["value"] *= 100
    month = pix_data["month"]
    year = pix_data["year"]
    dizimo_payment = await dizimo_payment_crud.get_payment_by_month_year_and_user_id(
        month, year, user.id
    )
    if dizimo_payment_is_paid(dizimo_payment):
        raise bad_request(f"Payment already paid")
    if dizimo_payment_is_expired(dizimo_payment):
        raise not_acceptable(f"Payment is expired")
    if dizimo_payment.correlation_id:
        pix_payment = get_pix_payment_from_correlation_id(dizimo_payment.correlation_id)
        if is_pix_active(pix_payment, pix_data["value"]):
            await pix_notification_message(
                "Pix ja foi gerado", "Realize o pagamento", user.id
            )
            return get_pix_no_sensitive_data(pix_payment)
    pix_info = PixInfo(
        value=pix_data["value"],
        pix_key=community.pix_key
    )
    pix_payment = PixPayment(
        value=pix_data["value"],
        customer=create_customer(user),
        correlationID=str(uuid4()),
        split=[pix_info]
    )
    pix_payment = make_post_pix_request(pix_payment)
    dizimo_payment = complete_dizimo_payment(dizimo_payment, pix_payment)
    await dizimo_payment_crud.complete_dizimo_payment(dizimo_payment)
    for i in range(1, 31):
        TIME = datetime.now() + timedelta(minutes=i)
        scheduler.add_job(
            update_payment_and_push_notification,
            DateTrigger(run_date=TIME),
            args=[dizimo_payment.correlation_id, i],
        )
    await pix_notification_message(
        "Pix gerado", "Realize o pagamento em ate 30 minutos", user.id
    )
    return get_pix_no_sensitive_data(pix_payment)


@router.get(
    "/dizimo_payment/{cpf}/{year}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_user_access_token)],
)
async def get_dizimo_payment_by_year_and_cpf_user_verify(
    cpf: str, year: int, user: dict = Depends(verify_user_access_token)
):
    user = await user_crud.get_user_by_cpf(user["cpf"])
    user_verify = await user_crud.get_user_by_cpf(cpf)
    dizimo_payments = await dizimo_payment_crud.get_payments_by_year_and_user_id(
        year, user_verify.id
    )
    return [
        get_dizimo_payment_no_sensitive_data(payment) for payment in dizimo_payments
    ]


@router.get(
    "/dizimo_payment/{year}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_user_access_token)],
)
async def get_dizimo_payment_by_year(
    year: int, user: dict = Depends(verify_user_access_token)
):
    user = await user_crud.get_user_by_cpf(user["cpf"])
    dizimo_payments = await dizimo_payment_crud.get_payments_by_year_and_user_id(
        year, user.id
    )
    return [
        get_dizimo_payment_no_sensitive_data(payment) for payment in dizimo_payments
    ]


@router.get(
    "/dizimo_payment/{year}/{month}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_user_access_token)],
)
async def get_dizimo_payment_by_year_and_month(
    year: int, month: str, user: dict = Depends(verify_user_access_token)
):
    user = await user_crud.get_user_by_cpf(user["cpf"])
    dizimo_payment = await dizimo_payment_crud.get_payment_by_month_year_and_user_id(
        month, year, user.id
    )
    return get_dizimo_payment_no_sensitive_data(dizimo_payment)


@router.get(
    "/get_all_user_dizimo_payments",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_user_access_token)],
)
async def get_all_user_payments(
    user: dict = Depends(verify_user_access_token),
):
    user = await user_crud.get_user_by_cpf(user["cpf"])
    async for dizimo_payments in dizimo_payment_crud.get_all_user_dizimo_payment(
        user.id
    ):

        async def dizimo_payment_generator():
            for dizimo_payment in dizimo_payments:
                payment = get_pix_payment_from_correlation_id(
                    dizimo_payment.correlation_id
                )
                yield json.dumps(get_pix_no_sensitive_data(payment)) + "\n"

    return StreamingResponse(dizimo_payment_generator(), media_type="application/json")
