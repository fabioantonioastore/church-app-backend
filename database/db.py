from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
from os import getenv

load_dotenv()

engine = create_async_engine(
    url = getenv("DATABASE_URL"),
    echo = False,
    pool_size = 5,
    max_overflow = 10,
    pool_pre_ping = True
)


class Base(DeclarativeBase):
    pass
