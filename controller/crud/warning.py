from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from typing import AsyncIterator
from models.warning import Warning
from controller.errors.http.exceptions import not_found, internal_server_error
from datetime import datetime
from database.session import session as db_session

SESSION = db_session


class WarningCrud:
    def __init__(self) -> None:
        self.session = SESSION

    async def get_warnings_by_community_id_from_pagination(self, community_id: str, page: int = 1,
                                                           page_size: int = 100) -> AsyncIterator:
        async with self.session() as session:
            try:
                offset = (page - 1) * page_size
                statement = select(Warning).filter(Warning.community_id == community_id).offset(offset).limit(page_size)
                warnings = await session.execute(statement)
                warnings = warnings.scalars().all()
                yield warnings
            except Exception as error:
                await session.rollback()
                raise internal_server_error(f"A error occurs during CRUD: {error!r}")

    async def get_warning_by_id(self, warning_id: str):
        async with self.session() as session:
            try:
                statement = select(Warning).filter(Warning.id == warning_id)
                warning = await session.execute(statement)
                return warning.scalars().one()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_warning_by_community_id(self, community_id: str, total: int = 10):
        async with self.session() as session:
            try:
                statement = select(Warning).filter(Warning.community_id == community_id).limit(total)
                warnings = await session.execute(statement)
                return warnings.scalars().all()
            except Exception as error:
                await session.rollback()
                raise internal_server_error(f"A error occurs during CRUD: {error!r}")

    async def create_warning(self, warning: Warning):
        async with self.session() as session:
            try:
                session.add(warning)
                await session.commit()
                return warning
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def update_warning(self, new_warning: dict):
        async with self.session() as session:
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
                warning.edited_at = datetime.now()
                await session.commit()
                return warning
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def delete_warning(self, warning: Warning):
        async with self.session() as session:
            try:
                await session.delete(warning)
                await session.commit()
                return f"{warning} deleted with succesfull"
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def delete_warning_by_id(self, warning_id: str):
        async with self.session() as session:
            try:
                statement = select(Warning).filter(Warning.id == warning_id)
                warning = await session.execute(statement)
                warning = warning.scalars().one()
                await session.delete(warning)
                await session.commit()
                return f"{warning} deleted with succesfull"
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")
