from pydantic import BaseModel
from datetime import datetime

class FinanceModel(BaseModel):
    id: str
    title: str
    description: str | None
    value: float
    community_id: str
    type: str
    date: datetime

class CreateFinanceModel(BaseModel):
    title: str
    description: str | None
    value: float
    type: str
    date: datetime | None

class UpdateFinanceModel(BaseModel):
    title: str | None
    description: str | None
    value: float | None
    type: str | None
    date: datetime | None
