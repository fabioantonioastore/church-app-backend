from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Text, ForeignKey, DateTime, LargeBinary
from datetime import datetime, timezone
from database import Base
from controller.src.generate_uuid import generate_uuid4


class Warning(Base):
    __tablename__ = 'warnings'

    id = mapped_column(String, primary_key=True, default=generate_uuid4)
    scope = mapped_column(String)
    title = mapped_column(String)
    description = mapped_column(Text)
    posted_at = mapped_column(DateTime, default=datetime.now)
    edited_at = mapped_column(DateTime, nullable=True)
    community_id = mapped_column(String, ForeignKey('communities.id'))
    image = mapped_column(LargeBinary, nullable=True)
