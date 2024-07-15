from sqlalchemy.orm import mapped_column
from sqlalchemy import String, ForeignKey, DateTime
from database.db import Base
from datetime import datetime

class Session(Base):
    __tablename__ = 'sessions'

    id = mapped_column(String, primary_key=True)
    user_id = mapped_column(String, ForeignKey('users.id'))
    token = mapped_column(String, unique=True)
    create_at = mapped_column(DateTime, default=datetime.now)
    last_accessed = mapped_column(DateTime)