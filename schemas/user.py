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

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "extra": {
                "cpf": "new cpf of the user or None",
                "email": "new email of the user or None",
                "name": "new name of the user or None",
                "community_patron": "new community of the user or None",
                "password": "new password of the user or None",
                "birthday": "new birthday of the user or None"
            }
        }
    )

class UpgradeUserPosition(BaseModel):
    cpf: str
    position: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "cpf": "cpf of the user",
                "position": "new position of the user"
            }
        }
    )