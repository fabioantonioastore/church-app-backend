from pydantic import BaseModel, ConfigDict, validator

class SignIn(BaseModel):
    cpf: str
    password: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "cpf": "cpf of the user",
                "password": "password of the user"
            }
        }
    )

class SignInAdmin(SignIn):
    position: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "cpf": "cpf of the user",
                "password": "password of the user",
                "position": "position of the user"
            }
        }
    )

class SignUp(BaseModel):
    cpf: str
    name: str
    password: str
    birthday: str
    community: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "cpf": "cpf of the user",
                "name": "name of the user",
                "password": "password of the user",
                "birthday": "birthday of the user",
                "community": "community name"
            }
        }
    )