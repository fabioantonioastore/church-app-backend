from sqlalchemy.ext.asyncio import async_sessionmaker
from database.db import engine

session = async_sessionmaker(bind=engine, expire_on_commit=False)