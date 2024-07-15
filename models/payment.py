from sqlalchemy.orm import mapped_column
from sqlalchemy import String, DateTime, Float, ForeignKey
from database.db import Base

class Payment(Base):
    __tablename__ = 'payments'

    id = mapped_column(String, primary_key=True)
    date = mapped_column(DateTime)
    type = mapped_column(String)
    value = mapped_column(Float)
    status = mapped_column(String)
    user_cpf = mapped_column(String, ForeignKey('users.cpf'))