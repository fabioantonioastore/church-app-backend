from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Date, LargeBinary
from database.db import Base

class User(Base):
    __tablename__ = 'users'

    id = mapped_column(String, primary_key=True)
    cpf = mapped_column(String, unique=True)
    name = mapped_column(String)
    birthday = mapped_column(Date)
    email = mapped_column(String, unique=True, nullable=True)
    position = mapped_column(String, nullable=True)
    image = mapped_column(LargeBinary, nullable=True)
    community_id = mapped_column(String, nullable=True)
    payments = relationship('Payment')