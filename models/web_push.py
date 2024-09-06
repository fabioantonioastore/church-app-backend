from database.db import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from controller.src.generate_uuid import generate_uuid4
from models.user import User


class WebPush(Base):
    __tablename__ = "web_push"

    id = mapped_column(String, primary_key=True, default=generate_uuid4)
    token = mapped_column(String, unique=True)
    user_id = mapped_column(String, ForeignKey("users.id"))

    user = relationship("User", back_populates="web_push")
