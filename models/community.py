from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, LargeBinary, Boolean
from database.db import Base
from models.warning import Warning

class Community(Base):
    __tablename__ = 'communities'

    id = mapped_column(String, primary_key=True)
    patron = mapped_column(String, unique=True)
    location = mapped_column(String)
    email = mapped_column(String, unique=True)
    image = mapped_column(LargeBinary)
    active = mapped_column(Boolean, default=True)
    warnings = relationship('Warning', cascade='all, delete-orphan')