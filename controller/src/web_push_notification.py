from models import WebPush
from controller.crud import WebPushCrud
from typing import NoReturn, NamedTuple
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from controller.jobs.web_push_notification import send_notification, execute_notification

web_push_crud = WebPushCrud()


class MessageNotification(NamedTuple):
    title: str
    body: str


def create_web_push_model(web_push_data: dict) -> WebPush:
    web_push = WebPush()
    web_push.token = web_push_data["token"]
    web_push.user_id = web_push_data["user_id"]
    return web_push


async def get_web_pushes() -> [WebPush]:
    async for web_pushes in web_push_crud.get_web_pushes_paginated():
        for web_push in web_pushes:
            yield web_push


def is_first_month_day(day: int) -> bool:
    return day == 1


def initiciate_push_notification_jobs(scheduler: AsyncIOScheduler) -> NoReturn:
    scheduler.add_job(send_notification, trigger=CronTrigger(day=1, hour=0, minute=0, second=0))
    for i in range(1, 31):
        for j in range(6, 19, 6):
            scheduler.add_job(send_notification, trigger=CronTrigger(day=i, hour=j, minute=0, second=0))


async def send_notification_to_user(user_id: str, message: MessageNotification) -> None:
    web_push = await web_push_crud.get_web_push_by_user_id(user_id)
    token = web_push.token
    execute_notification(token, message.title, message.body)
