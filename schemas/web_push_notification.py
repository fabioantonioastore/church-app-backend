from pydantic import BaseModel, ConfigDict


class PushSubscription(BaseModel):
    endpoint: str
    p256dh: str
    auth: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "endpoint": "endpoint of device",
                "p256dh": "public key",
                "auth": "auth key"
            }
        }
    )


class PushNotification(BaseModel):
    title: str
    body: str
    subscription: PushSubscription
