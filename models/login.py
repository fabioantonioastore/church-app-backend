from sqlalchemy.orm import mapped_column
from sqlalchemy import String, ForeignKey
from database.db import Base

class Login(Base):
    __tablename__ = 'logins'

    id = mapped_column(String, primary_key=True)
    cpf = mapped_column(String, ForeignKey('users.cpf'), unique=True)
    password = mapped_column(String)
    position = mapped_column(String, default='user')