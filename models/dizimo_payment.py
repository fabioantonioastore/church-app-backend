from sqlalchemy.orm import mapped_column
from sqlalchemy import String, DateTime, Float, ForeignKey, Integer
from database.db import Base

class DizimoPayment(Base):
    __tablename__ = 'payments'

    id = mapped_column(String, primary_key=True)
    correlation_id = mapped_column(String, nullable=True, unique=True)
    identifier = mapped_column(String, nullable=True, unique=True)
    date = mapped_column(DateTime, nullable=True)
    month = mapped_column(String)
    year = mapped_column(Integer)
    value = mapped_column(Float, nullable=True)
    status = mapped_column(String)
    user_id = mapped_column(String, ForeignKey('users.id'))