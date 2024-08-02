from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select
from models.user import User
from controller.errors.http.exceptions import not_found

class UserCrud:
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
                        case 'name':
                            user.name = new_user['name']
                        case 'birthday':
                            user.birthday = new_user['birthday']
                        case 'email':
                            user.email = new_user['email']
                        case 'community_id':
                            user.community_id = new_user['community_id']
                        case 'image':
                            user.image = new_user['image']
                        case 'active':
                            user.active = new_user['active']
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