from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, DateTime, Float, ForeignKey, Integer
from database.db import Base
from controller.src.generate_uuid import generate_uuid4


class DizimoPayment(Base):
    __tablename__ = 'payments'

    id = mapped_column(String, primary_key=True, default=generate_uuid4)
    correlation_id = mapped_column(String, nullable=True, unique=True)
    date = mapped_column(DateTime, nullable=True)
    month = mapped_column(String)
    year = mapped_column(Integer)
    value = mapped_column(Float, nullable=True)
    status = mapped_column(String)
    user_id = mapped_column(String, ForeignKey('users.id'))

    user = relationship("User", back_populates="dizimo_payments")
