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
    pix_key: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "patron": "patron of the community",
                "location": "location of the community",
                "email": "email of the community",
                "image": "image of the community or None",
            }
        },
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
                "patron": "new patron of the community or None",
                "location": "new location of the community or None",
                "email": "new email of the community or None",
                "image": "new image of the community or None",
            }
        },
    )


class DeleteCommunityModel(BaseModel):
    patron: str | None = None
    id: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "patron": "patron of the community or None",
                "id": "id of the community or None",
            }
        },
    )
