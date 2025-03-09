from pydantic import BaseModel


class DizimoPaymentModel(BaseModel):
    pass


class CreateDizimoPaymentModel(BaseModel):
    value: int | float
    month: str
    year: int
