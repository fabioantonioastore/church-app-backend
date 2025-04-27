from database.db import Base, engine
import asyncio
from sqlalchemy import text


async def create_db():
    async with engine.begin() as conn:
        await conn.execute(text("DROP TABLE alembic_version;"))

    await engine.dispose()


asyncio.run(create_db())
