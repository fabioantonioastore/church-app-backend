from pydantic import BaseModel, ConfigDict

class CommunityModel(BaseModel):
    id: str
    patron: str
    location: str
    email: str
    image: str
    active: bool

class CreateCommunityModel(BaseModel):
    patron: str
    location: str
    email: str
    image: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "patron": "patron of the community",
                "location": "location of the community",
                "email": "email of the community",
                "image": "image of the community or None"
            }
        }
    )

class UpdateCommunityModel(BaseModel):
    patron: str | None = None
    location: str | None = None
    email: str | None = None
    image: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "patron": "patron of the community or None",
                "location": "loation of the community or None",
                "email": "email of the community or None",
                "image": "image of the community or None"
            }
        }
    )

class DeleteCommunityModel(BaseModel):
    patron: str | None = None
    id: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "patron": "patron of the community or None",
                "id": "id of the community or None"
            }
        }
    )

class UpdateCommunityPatron(BaseModel):
    patron: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "patron": "new patron of the community"
            }
        }
    )

class UpdateCommunityLocation(BaseModel):
    location: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "location": "new location of the community"
            }
        }
    )

class UpdateCommunityEmail(BaseModel):
    email: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "email": "new email of the community"
            }
        }
    )

class UpdateCommunityImage(BaseModel):
    image: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "image": "new image of the community"
            }
        }
    )