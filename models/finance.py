from sqlalchemy.orm import mapped_column
from sqlalchemy import String, ForeignKey, DateTime, Integer, Float
from database import Base
from controller.src.generate_uuid import generate_uuid4
from datetime import datetime


class Finance(Base):
    __tablename__ = 'finances'

    id = mapped_column(String, primary_key=True, default=generate_uuid4)
    community_id = mapped_column(String, ForeignKey('communities.id'))
    title = mapped_column(String)
    description = mapped_column(String, nullable=True)
    date = mapped_column(DateTime, default=datetime.now)
    month = mapped_column(String)
    year = mapped_column(Integer)
    value = mapped_column(Float, nullable=True)
    amount = mapped_column(Integer, nullable=True)
    hours = mapped_column(Integer, nullable=True)
    type = mapped_column(String)
