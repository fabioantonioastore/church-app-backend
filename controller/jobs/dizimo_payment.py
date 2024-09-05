from typing import NoReturn
from controller.crud.dizimo_payment import DizimoPaymentCrud
from controller.src.pix_payment import get_pix_payment_from_correlation_id
from controller.src.pix_payment import is_pix_paid, is_pix_expired, is_pix_active
from controller.src.pix_payment import delete_pix_by_correlation_id, get_pix_value
from models.user import User
from controller.crud.user import UserCrud
from controller.crud.community import CommunityCrud
from controller.src.dizimo_payment import create_dizimo_payment, get_dizimo_status
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

dizimo_payment_crud = DizimoPaymentCrud()
user_crud = UserCrud()
community_crud = CommunityCrud()
scheduler = AsyncIOScheduler()

PAID = "paid"
EXPIRED = "expired"
ACTIVE = "active"


async def update_payment_and_push_notification(correlation_id: str, user: User = None) -> NoReturn:
    dizimo_payment = await dizimo_payment_crud.get_payment_by_correlation_id(correlation_id)
    pix_payment = get_pix_payment_from_correlation_id(dizimo_payment.correlation_id)
    if get_dizimo_status(dizimo_payment) == ACTIVE:
        if is_pix_paid(pix_payment):
            await dizimo_payment_crud.update_status(dizimo_payment.id, PAID)
            if not user:
                user = await user_crud.get_user_by_id(dizimo_payment.user_id)
            await community_crud.increase_actual_month_payment_value(user.community_id, get_pix_value(pix_payment))
            remove_jobs_by_function(update_payment_and_push_notification)
            return
        if is_pix_expired(pix_payment):
            delete_pix_by_correlation_id(dizimo_payment.correlation_id)
            await dizimo_payment_crud.update_correlation_id_to_none(dizimo_payment.id)
            return
        if is_pix_active(pix_payment):
            return
    if get_dizimo_status(dizimo_payment) == PAID:
        remove_jobs_by_function(update_payment_and_push_notification)


def remove_jobs_by_function(func):
    jobs = scheduler.get_jobs()
    for job in jobs:
        if job.func == func:
            scheduler.remove_job(job.id)


async def create_month_dizimo_payment_and_transfer_payments_values() -> NoReturn:
    async for users in user_crud.get_users_paginated():
        for user in users:
            dizimo_payment = await create_dizimo_payment(user)
            await dizimo_payment_crud.create_payment(dizimo_payment)
    async for communities in community_crud.get_communities_paginated():
        for community in communities:
            await community_crud.transfer_actual_to_last_month_and_reset_actual(community.id)
