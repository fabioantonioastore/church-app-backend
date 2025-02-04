from pydantic import BaseModel, ConfigDict


class PushSubscription(BaseModel):
    token: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"token": "Token of device"}},
    )


class PushNotification(BaseModel):
    title: str
    body: str
    token: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "title": "Title of the notification",
                "body": "Body of the notification",
                "token": "Token of the device",
            }
        },
    )
