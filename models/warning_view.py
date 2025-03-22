from sqlalchemy.orm import mapped_column
from sqlalchemy import String, ForeignKey, DateTime
from datetime import datetime
from database import Base
from controller.src.generate_uuid import generate_uuid4


class WarningView(Base):
    __tablename__ = "warnings_view"

    id = mapped_column(String, primary_key=True, default=generate_uuid4)
    warning_id = mapped_column(String)
    cpf = mapped_column(String)
    date = mapped_column(DateTime, default=datetime.now)