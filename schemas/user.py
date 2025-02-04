from pydantic import BaseModel, ConfigDict


class UserModel(BaseModel):
    id: str
    cpf: str
    name: str
    birthday: str
    phone: str
    position: str
    image: str
    community_id: str
    active: bool


class CreateUserModel(UserModel):
    pass


class UpdateUserModel(BaseModel):
    cpf: str
    phone: str
    name: str
    community_patron: str
    password: str
    birthday: str
    image: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "extra": {
                "cpf": "new cpf of the user",
                "phone": "new phone of the user",
                "name": "new name of the user",
                "community_patron": "new community of the user",
                "password": "new password of the user",
                "birthday": "new birthday of the user",
                "image": "image of the user",
            }
        },
    )


class UpgradeUserPositionResponsability(BaseModel):
    cpf: str
    position: str
    responsibility: str | None = "member"

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "cpf": "cpf of the user",
                "position": "new position of the user",
                "responsibility": "responsibility of the user or None",
            }
        },
    )
