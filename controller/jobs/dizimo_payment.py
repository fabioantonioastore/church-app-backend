import datetime
from typing import NoReturn
from controller.crud.dizimo_payment import DizimoPaymentCrud
from controller.src.pix_payment import get_pix_payment_from_correlation_id
from controller.src.pix_payment import (
    is_pix_paid,
    is_pix_expired,
    is_pix_active,
    withdraw_from_subaccount
)
from controller.src.pix_payment import (
    delete_pix_by_correlation_id,
    get_pix_value,
)
from models.user import User
from controller.crud.user import UserCrud
from controller.crud.community import CommunityCrud
from controller.src.dizimo_payment import (
    create_dizimo_payment,
    get_dizimo_status,
    convert_to_month,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from firebase_admin import messaging
from controller.crud.web_push import WebPushCrud


dizimo_payment_crud = DizimoPaymentCrud()
user_crud = UserCrud()
community_crud = CommunityCrud()
web_push_crud = WebPushCrud()
scheduler = AsyncIOScheduler()

PAID = "paid"
EXPIRED = "expired"
ACTIVE = "active"


async def update_payment_and_push_notification(
    correlation_id: str, count: int = 0
) -> NoReturn:
    dizimo_payment = await dizimo_payment_crud.get_payment_by_correlation_id(
        correlation_id
    )
    pix_payment = get_pix_payment_from_correlation_id(dizimo_payment.correlation_id)
    user = await user_crud.get_user_by_id(dizimo_payment.user_id)
    if get_dizimo_status(dizimo_payment) == ACTIVE:
        if is_pix_paid(pix_payment):
            await dizimo_payment_crud.update_status(dizimo_payment.id, PAID)
            await community_crud.increase_actual_month_payment_value(
                user.community_id, get_pix_value(pix_payment)
            )
            await pix_notification_message(
                "E-Igreja",
                "Pagamento confirmado, obrigado pela a sua doacao",
                user.id,
            )
            remove_jobs_by_function(
                update_payment_and_push_notification, correlation_id
            )
            return
        if is_pix_expired(pix_payment):
            delete_pix_by_correlation_id(dizimo_payment.correlation_id)
            await dizimo_payment_crud.update_correlation_id_to_none(dizimo_payment.id)
            await pix_notification_message(
                "E-Igreja", "Pix expirado, por favor gerar outro pix", user.id
            )
            remove_jobs_by_function(
                update_payment_and_push_notification, correlation_id
            )
            return
        if is_pix_active(pix_payment):
            if count == 5 or count == 10 or count == 15 or count == 20 or count == 25:
                await pix_notification_message(
                    "E-Igreja",
                    f"Realize o pagamento, ainda falta {30 - count} minutos para realizar o pagamento",
                    user.id,
                )
            return
    if get_dizimo_status(dizimo_payment) == PAID:
        remove_jobs_by_function(update_payment_and_push_notification, correlation_id)


async def pix_notification_message(title: str, body: str, user_id: str) -> NoReturn:
    try:
        web_push = await web_push_crud.get_web_push_by_user_id(user_id)
        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            token=web_push.token,
        )
        messaging.send(message)
    except Exception as error:
        print(error)


def remove_jobs_by_function(func, correlation_id: str) -> NoReturn:
    jobs = scheduler.get_jobs()
    for job in jobs:
        if job.func == func and job.kwargs.get("correlation_id") == correlation_id:
            scheduler.remove_job(job.id)


async def create_month_dizimo_payment_and_transfer_payments_values() -> NoReturn:
    async for users in user_crud.get_users_paginated():
        for user in users:
            dizimo_payment = await create_dizimo_payment(user)
            await dizimo_payment_crud.create_payment(dizimo_payment)
    async for communities in community_crud.get_communities_paginated():
        for community in communities:
            await community_crud.transfer_actual_to_last_month_and_reset_actual(
                community.id
            )


async def set_dizimo_payments_expired() -> None:
    month = datetime.datetime.now().month
    month = convert_to_month(month)
    async for dizimo_payments in dizimo_payment_crud.get_payments_by_status_paginated(
        "active"
    ):
        for dizimo in dizimo_payments:
            if dizimo.month != month:
                continue
            dizimo_payment_update = {
                "id": dizimo.id,
                "correlation_id": None,
                "status": "expired",
            }
            await dizimo_payment_crud.update_payment(dizimo_payment_update)
