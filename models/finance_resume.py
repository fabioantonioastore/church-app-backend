from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Float, ForeignKey
from database.db import Base
from controller.src.generate_uuid import generate_uuid4


class FinanceResume(Base):
    __tablename__ = "finance_resumes"

    id = mapped_column(String, primary_key=True, default=generate_uuid4)
    last_month_id = mapped_column(String, ForeignKey("finances.id"), unique=True, nullable=True)
    recipe = mapped_column(Float)
    input = mapped_column(Float)
    output = mapped_column(Float)
    community_id = mapped_column(String, ForeignKey("communities.id"))
