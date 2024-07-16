from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from models.session import Session
from controller.errors.database_error import DatabaseError

class SessionCrud:
    async def get_session_by_id(self, async_session: async_sessionmaker[AsyncSession], session_id: str):
        async with async_session() as session:
            try:
                statement = select(Session).filter(Session.id == session_id)
                session_data = await session.execute(statement)
                return session_data.scalars().one()
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def get_session_by_user_id(self, async_session: async_sessionmaker[AsyncSession], session_user_id: str):
        async with async_session() as session:
            try:
                statement = select(Session).filter(Session.user_id == session_user_id)
                session_data = await session.execute(statement)
                return session_data.scalars().one()
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def get_session_by_token(self, async_session: async_sessionmaker[AsyncSession], session_toke: str):
        async with async_session() as session:
            try:
                statement = select(Session).filter(Session.token == session_toke)
                session_data = await session.execute(statement)
                return session_data.scalars().one()
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def create_session(self, async_session: async_sessionmaker[AsyncSession], session_data: Session):
        async with async_session() as session:
            try:
                session.add(session_data)
                await session.commit()
                return session_data
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def update_session(self, async_session: async_sessionmaker[AsyncSession], new_session: dict):
        async with async_session() as session:
            try:
                statement = select(Session).filter(Session.id == new_session['id'])
                session_data = await session.execute(statement)
                session_data = session_data.scalars().one()
                for key in new_session.keys():
                    match key:
                        case 'token':
                            session_data.token = new_session['token']
                        case 'create_at':
                            session_data.create_at = new_session['create_at']
                        case 'last_accessed':
                            session_data.last_accessed = new_session['last_accessed']
                await session.commit()
                return session_data
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def delete_session(self, async_session: async_sessionmaker[AsyncSession], session_data: Session):
        async with async_session() as session:
            try:
                await session.delete(session_data)
                await session.commit()
                return f"{session_data} deleted with succesfull"
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def delete_session_by_id(self, async_session: async_sessionmaker[AsyncSession], session_id: str):
        async with async_session() as session:
            try:
                statement = select(Session).filter(Session.id == session_id)
                session_data = await session.execute(statement)
                session_data = session_data.scalars().one()
                await session.delete(session_data)
                await session.commit()
                return f"{session_data} deleted with succesfull"
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error