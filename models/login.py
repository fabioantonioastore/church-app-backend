from sqlalchemy.orm import mapped_column
from sqlalchemy import String, ForeignKey
from database import Base
from controller.src.generate_uuid import generate_uuid4


class Login(Base):
    __tablename__ = 'logins'

    id = mapped_column(String, primary_key=True, default=generate_uuid4)
    cpf = mapped_column(String, ForeignKey('users.cpf'), unique=True)
    password = mapped_column(String)
    position = mapped_column(String, default='user')