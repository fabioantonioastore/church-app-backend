from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Date, LargeBinary, ForeignKey, Boolean
from database import Base
from controller.src.generate_uuid import generate_uuid4
from models.web_push import WebPush


class User(Base):
    __tablename__ = "users"

    id = mapped_column(String, primary_key=True, default=generate_uuid4)
    cpf = mapped_column(String, unique=True)
    name = mapped_column(String)
    birthday = mapped_column(Date)
    phone = mapped_column(String, unique=True)
    position = mapped_column(String, default="user")
    image = mapped_column(String, nullable=True)
    active = mapped_column(Boolean, default=True)
    community_id = mapped_column(String, ForeignKey("communities.id"))
    responsibility = mapped_column(String, default="faithful")

    dizimo_payments = relationship("DizimoPayment", back_populates="user")
    web_push = relationship(
        "WebPush", back_populates="user", cascade="all, delete-orphan"
    )
    number = relationship("Number", back_populates="user", cascade="all, delete-orphan")
