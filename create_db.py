from database.db import Base, engine
import asyncio

async def create_db():
    async with engine.begin() as conn:
        from models.user import User
        from models.login import Login
        from models.payment import Payment
        from models.session import Session
        from models.warning import Warning
        from models.board_member import BoardMember
        from models.community import Community

        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()

asyncio.run(create_db())