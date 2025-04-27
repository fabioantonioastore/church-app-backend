from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Boolean, Integer
from database import Base
from controller.src.generate_uuid import generate_uuid4


class Cleaning(Base):
    __tablename__ = "cleaning"

    id = mapped_column(String, primary_key=True, default=generate_uuid4)
    name = mapped_column(String)
    setor = mapped_column(Integer)
    payed = mapped_column(Boolean)
    month = mapped_column(String)
    year = mapped_column(Integer)
