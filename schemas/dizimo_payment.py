from pydantic import BaseModel


class DizimoPaymentModel(BaseModel):
    pass


class CreateDizimoPaymentModel(BaseModel):
    value: float
    month: str
    year: int
