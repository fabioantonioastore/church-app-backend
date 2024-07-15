from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Text, ForeignKey, Integer
from database.db import Base

class Warning(Base):
    __tablename__ = 'warnings'

    id = mapped_column(String, primary_key=True)
    scope = mapped_column(Integer)
    title = mapped_column(String)
    description = mapped_column(Text)
    community_id = mapped_column(String, ForeignKey('communities.id'))