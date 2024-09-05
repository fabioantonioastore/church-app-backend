from pywebpush import webpush, WebPushException
from schemas.web_push_notification import PushSubscription
from controller.src.web_push_notification import create_web_push_model
from models.user import User
from models.web_push import WebPush
from controller.crud.web_push import WebPushCrud
from fastapi import APIRouter, Depends, status
from controller.crud.user import UserCrud
from router.middleware.authorization import verify_user_access_token
from controller.auth.vapid import VAPID_PRIVATE_KEY, VAPID_CLAIMS
from controller.errors.http.exceptions import internal_server_error

router = APIRouter()
web_push_crud = WebPushCrud()
user_crud = UserCrud()


@router.post("/web_push/subscription", status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_user_access_token)])
async def subscribe(subscription: PushSubscription, user: dict = Depends(verify_user_access_token)) -> str:
    subscription = dict(subscription)
    user = await user_crud.get_user_by_cpf(user["cpf"])
    subscription["user_id"] = user.id
    web_push = create_web_push_model(subscription)
    await web_push_crud.create_web_push(web_push)
    return "Subscription realized"


@router.post("/web_push/send_notification", status_code=status.HTTP_200_OK)
async def send_notification(subscription: PushSubscription, message: str):
    try:
        KEYS = {"p256dh": subscription.p256dh,
                "auth": subscription.auth
                }
        webpush(
            subscription_info={
                "endpoint": subscription.endpoint,
                "keys": KEYS
            },
            data=message,
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims=VAPID_CLAIMS
        )
        return "Notification sent"
    except WebPushException as error:
        raise internal_server_error(str(error))
