from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select, and_, or_
from models.user import User
from models.dizimo_payment import DizimoPayment
from controller.errors.http.exceptions import not_found, internal_server_error
from controller.crud.community import CommunityCrud
from database.session import session as db_session
from typing import AsyncIterator

community_crud = CommunityCrud()

class UserCrud:
    async def get_users_paginated(self, async_session: async_sessionmaker[AsyncSession], page: int = 1, page_size: int = 100) -> AsyncIterator:
        async with async_session() as session:
            offset = (page - 1) * page_size
            try:
                statement = select(User).offset(offset).limit(page_size)
                users = await session.execute(statement)
                users = users.scalars().all()
                yield users
            except Exception as error:
                await session.rollback()
                raise internal_server_error(f"A error occurs during CRUD: {error!r}")

    async def get_all_users(self, async_session: async_sessionmaker[AsyncSession]) -> [User]:
        async with async_session() as session:
            try:
                statement = select(User)
                users = await session.execute(statement)
                return users.scalars().all()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def upgrade_user(self, async_session: async_sessionmaker[AsyncSession], cpf: str, position: str, responsability: str):
        async with async_session() as session:
            try:
                statement = select(User).filter(User.cpf == cpf)
                user = await session.execute(statement)
                user = user.scalars().one()
                user.position = position
                user.responsibility = responsability
                await session.commit()
                return user
            except Exception as error:
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_all_community_council_and_parish(self, async_session: async_sessionmaker[AsyncSession], community_id: str):
        async with async_session() as session:
            try:
                statement = select(User).filter(
                    and_(
                        User.community_id == community_id,
                        or_(
                            User.position == "parish leader",
                            User.position == "council member"
                        )
                    )
                )
                users = await session.execute(statement)
                return users.scalars().all()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")
    async def get_users_by_community_id(self, async_session: async_sessionmaker[AsyncSession], community_id: str):
        async with async_session() as session:
            try:
                statement = select(User).filter(User.community_id == community_id)
                users = await session.execute(statement)
                return users.scalars().all()
            except Exception as error:
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_user_by_id(self, async_session: async_sessionmaker[AsyncSession], user_id: str):
        async with async_session() as session:
            try:
                statement = select(User).filter(User.id == user_id)
                user = await session.execute(statement)
                return user.scalars().one()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_user_by_cpf(self, async_session: async_sessionmaker[AsyncSession], user_cpf: str):
        async with async_session() as session:
            try:
                statement = select(User).filter(User.cpf == user_cpf)
                user = await session.execute(statement)
                return user.scalars().one()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_user_by_phone(self, async_session: async_sessionmaker[AsyncSession], phone: str) -> User:
        async with async_session() as session:
            try:
                statement = select(User).filter(User.phone == phone)
                user = await session.execute(statement)
                return user.scalars().one()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def create_user(self, async_session: async_sessionmaker[AsyncSession], user: User):
        async with async_session() as session:
            try:
                session.add(user)
                await session.commit()
                return user
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def update_user(self, async_session: async_sessionmaker[AsyncSession], new_user: dict):
        async with async_session() as session:
            try:
                statement = select(User).filter(User.id == new_user['id'])
                user = await session.execute(statement)
                user = user.scalars().one()
                for key in new_user.keys():
                    match key:
                        case 'cpf':
                            if new_user['cpf'] != user.cpf:
                                user.cpf = new_user['cpf']
                        case 'name':
                            user.name = new_user['name']
                        case 'birthday':
                            user.birthday = new_user['birthday']
                        case 'phone':
                            user.phone = new_user['phone']
                        case 'community_id':
                            user.community_id = new_user['community_id']
                        case 'image':
                            user.image = new_user['image']
                        case 'active':
                            user.active = new_user['active']
                        case 'community_patron':
                            community = await community_crud.get_community_by_patron(db_session, new_user['community_patron'])
                            user.community_id = community.id
                await session.commit()
                return user
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def delete_user(self, async_session: async_sessionmaker[AsyncSession], user: User):
        async with async_session() as session:
            try:
                await session.delete(user)
                await session.commit()
                return f"{user} deleted with succesfull"
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def delete_user_by_id(self, async_session: async_sessionmaker[AsyncSession], user_id: str):
        async with async_session() as session:
            try:
                statement = select(User).filter(User.id == user_id)
                user = await session.execute(statement)
                user = user.scalars().one()
                await session.delete(user)
                await session.commit()
                return f"{user} deleted with succesfull"
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")