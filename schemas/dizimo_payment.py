from pydantic import BaseModel


class DizimoPaymentModel(BaseModel):
    pass


class CreateDizimoPaymentModel(BaseModel):
    value: int
    month: str
    year: int
