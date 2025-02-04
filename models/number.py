from database.db import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, ForeignKey
from controller.src.generate_uuid import generate_uuid4


class Number(Base):
    __tablename__ = "numbers"

    id = mapped_column(String, default=generate_uuid4, primary_key=True)
    user_id = mapped_column(String, ForeignKey("users.id"))
    number = mapped_column(String, unique=True)
    verification_code = mapped_column(Integer, nullable=True)
    valid = mapped_column(Boolean, default=False)

    user = relationship("User", back_populates="number")
