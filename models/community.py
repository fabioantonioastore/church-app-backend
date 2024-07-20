from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, LargeBinary
from database.db import Base
from models.warning import Warning

class Community(Base):
    __tablename__ = 'communities'

    id = mapped_column(String, primary_key=True)
    name = mapped_column(String, unique=True)
    patron = mapped_column(String)
    location = mapped_column(String, unique=True)
    email = mapped_column(String, unique=True)
    image = mapped_column(LargeBinary)
    warnings = relationship('Warning', cascade='all, delete-orphan')