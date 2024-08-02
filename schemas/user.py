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
    cpf: str
    email: str
    name: str
    community_patron: str
    password: str
    birthday: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "extra": {
                "cpf": "new cpf of the user",
                "email": "new email of the user",
                "name": "new name of the user",
                "community_patron": "new community of the user",
                "password": "new password of the user",
                "birthday": "new birthday of the user"
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