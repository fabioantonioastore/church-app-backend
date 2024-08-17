from pydantic import BaseModel, ConfigDict

class UserModel(BaseModel):
    id: str
    cpf: str
    name: str
    birthday: str
    email: str
    position: str
    image: str
    community_id: str
    active: bool

class CreateUserModel(UserModel):
    pass

class UpdateUserModel(BaseModel):
    cpf: str | None = None
    email: str | None = None
    name: str | None = None
    community_patron: str | None = None
    password: str | None = None
    birthday: str | None = None
    image: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "extra": {
                "cpf": "new cpf of the user",
                "email": "new email of the user",
                "name": "new name of the user",
                "community_patron": "new community of the user",
                "password": "new password of the user",
                "birthday": "new birthday of the user",
                "image": "image of the user"
            }
        }
    )

class UpgradeUserPosition(BaseModel):
    cpf: str
    position: str
    responsibility: str | None = "faithful"

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "cpf": "cpf of the user",
                "position": "new position of the user",
                "responsibility": "responsibility of the user or None"
            }
        }
    )