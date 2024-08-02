from pydantic import BaseModel, ConfigDict

class WarningModel(BaseModel):
    id: str
    scope: str
    title: str
    description: str
    posted_at: str
    edited_at: str
    community_id: str
    image: str

class CreateWarningModel(BaseModel):
    scope: str
    title: str
    description: str
    image: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "scope": "all or private",
                "title": "title of the warning",
                "description": "description of the warning",
                "image": "image of the warning or None"
            }
        }
    )

class UpdateWarningModel(BaseModel):
    title: str | None = None
    description: str | None = None
    scope: str | None = None
    image: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "title": "new title or None",
                "description": "new description or None",
                "scope": "all or private or None",
                "image": "image of warning or None"
            }
        }
    )

class DeleteWarningModel(BaseModel):
    id: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "id of the warning"
            }
        }
    )