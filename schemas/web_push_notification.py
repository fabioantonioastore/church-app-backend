from pydantic import BaseModel


class PushSubscription(BaseModel):
    endpoint: str
    p256dh: str
    auth: str


class PushNotification(BaseModel):
    title: str
    body: str
    subscription: PushSubscription
