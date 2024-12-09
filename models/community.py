from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, LargeBinary, Boolean, ForeignKey, Float
from database import Base
from models.warning import Warning
from controller.src.generate_uuid import generate_uuid4


class Community(Base):
    __tablename__ = 'communities'

    id = mapped_column(String, primary_key=True, default=generate_uuid4)
    patron = mapped_column(String, unique=True)
    location = mapped_column(String)
    email = mapped_column(String, unique=True)
    image = mapped_column(String, nullable=True)
    active = mapped_column(Boolean, default=True)
    actual_month_total_payment_value = mapped_column(Float, default=0)
    last_month_total_payment_value = mapped_column(Float, default=0)
    available_money = mapped_column(Float, default=0)

    warnings = relationship('Warning', cascade='all, delete-orphan')
    users = relationship('User')