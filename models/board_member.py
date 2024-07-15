from sqlalchemy.orm import mapped_column
from sqlalchemy import String, ForeignKey
from database.db import Base

class BoardMember(Base):
    __tablename__ = 'board_members'

    id = mapped_column(String, primary_key=True)
    user_id = mapped_column(String, ForeignKey('users.id'), unique=True)
    cpf = mapped_column(String, ForeignKey('users.cpf'), unique=True)
    position = mapped_column(String)