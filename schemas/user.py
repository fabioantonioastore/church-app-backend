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

class CreateUserModel(UserModel):
    pass

class UpdateUserPassword(BaseModel):
    password: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "password": "new password of the user"
            }
        }
    )

class UpdateUserName(BaseModel):
    name: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "new name of the user"
            }
        }
    )

class UpdateUserEmail(BaseModel):
    email: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "email": "new email of the user"
            }
        }
    )

class UpdateUserCommunity(BaseModel):
    patron: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "patron": "patron of the new community"
            }
        }
    )

class UpdateUserImage(BaseModel):
    image: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "image": "new user image"
            }
        }
    )

class UpdateUserBirthday(BaseModel):
    birthday: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
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