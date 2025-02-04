from database.db import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, LargeBinary, ForeignKey
from controller.src.generate_uuid import generate_uuid4


class Image(Base):
    __tablename__ = "images"

    id = mapped_column(String, primary_key=True, default=generate_uuid4)
    byte = mapped_column(LargeBinary, nullable=True)
