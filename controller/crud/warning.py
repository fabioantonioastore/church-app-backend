from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from models.warning import Warning
from controller.errors.database_error import DatabaseError

class WarningCrud:
    async def get_warning_by_id(self, async_session: async_sessionmaker[AsyncSession], warning_id: str):
        async with async_session() as session:
            try:
                statement = select(Warning).filter(Warning.id == warning_id)
                warning = await session.execute(statement)
                return warning.scalars().one()
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def get_warning_by_community_id(self, async_session: async_sessionmaker[AsyncSession], community_id: str, total_warnings=10):
        async with async_session() as session:
            try:
                statement = select(Warning).filter(Warning.community_id == community_id)
                warnings = await session.execute(statement)
                return warnings.scalars().all().count(total_warnings)
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def create_warning(self, async_session: async_sessionmaker[AsyncSession], warning: Warning):
        async with async_session() as session:
            try:
                session.add(warning)
                await session.commit()
                return warning
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def update_warning(self, async_session: async_sessionmaker[AsyncSession], new_warning: dict):
        async with async_session() as session:
            try:
                statement = select(Warning).filter(Warning.id == new_warning['id'])
                warning = await session.execute(statement)
                warning = warning.scalars().one()
                for key in new_warning.keys():
                    match key:
                        case 'scope':
                            warning.scope = new_warning['scope']
                        case 'title':
                            warning.title = new_warning['title']
                        case 'description':
                            warning.description = new_warning['description']
                        case 'edited_at':
                            warning.edited_in = new_warning['edited_at']
                await session.commit()
                return warning
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def delete_warning(self, async_session: async_sessionmaker[AsyncSession], warning: Warning):
        async with async_session() as session:
            try:
                await session.delete(warning)
                await session.commit()
                return f"{warning} deleted with succesfull"
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def delete_warning_by_id(self, async_session: async_sessionmaker[AsyncSession], warning_id: str):
        async with async_session() as session:
            try:
                statement = select(Warning).filter(Warning.id == warning_id)
                warning = await session.execute(statement)
                warning = warning.scalars().one()
                await session.delete(warning)
                await session.commit()
                return f"{warning} deleted with succesfull"
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error