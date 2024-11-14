from sqlalchemy import select, and_, or_
from models import User
from controller.errors.http.exceptions import not_found, internal_server_error
from controller.crud.community import CommunityCrud
from controller.crud.crud import CRUD
from typing import AsyncIterator

community_crud = CommunityCrud()


class UserCrud(CRUD):
    def __init__(self) -> None:
        super().__init__()

    async def get_users_paginated(self, page: int = 1, page_size: int = 100) -> AsyncIterator:
        async with self.session() as session:
            try:
                offset = (page - 1) * page_size
                statement = select(User).offset(offset).limit(page_size)
                users = await session.execute(statement)
                users = users.scalars().all()
                yield users
            except Exception as error:
                await session.rollback()
                raise internal_server_error(f"A error occurs during CRUD: {error!r}")

    async def get_all_users(self) -> [User]:
        async with self.session() as session:
            try:
                statement = select(User)
                users = await session.execute(statement)
                return users.scalars().all()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def upgrade_user(self, cpf: str, position: str, responsability: str):
        async with self.session() as session:
            try:
                statement = select(User).filter(User.cpf == cpf)
                user = await session.execute(statement)
                user = user.scalars().first()
                user.position = position
                user.responsibility = responsability
                await session.commit()
                return user
            except Exception as error:
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_all_community_council_and_parish(self, community_id: str):
        async with self.session() as session:
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

    async def get_users_by_community_id(self, community_id: str):
        async with self.session() as session:
            try:
                statement = select(User).filter(User.community_id == community_id)
                users = await session.execute(statement)
                return users.scalars().all()
            except Exception as error:
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_user_by_id(self, user_id: str):
        async with self.session() as session:
            try:
                statement = select(User).filter(User.id == user_id)
                user = await session.execute(statement)
                return user.scalars().first()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_user_by_cpf(self, user_cpf: str):
        async with self.session() as session:
            try:
                statement = select(User).filter(User.cpf == user_cpf)
                user = await session.execute(statement)
                return user.scalars().first()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_user_by_phone(self, phone: str) -> User:
        async with self.session() as session:
            try:
                statement = select(User).filter(User.phone == phone)
                user = await session.execute(statement)
                return user.scalars().first()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def create_user(self, user: User):
        async with self.session() as session:
            try:
                session.add(user)
                await session.commit()
                return user
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_user_image(self, user_cpf: str):
        async with self.session() as session:
            try:
                statement = select(User).filter(User.cpf == user_cpf)
                user = await session.execute(statement)
                user = user.scalars().first()
                return user.image
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def update_user_image(self, user_cpf: str, image: str):
        async with self.session() as session:
            try:
                statement = select(User).filter(User.cpf == user_cpf)
                user = await session.execute(statement)
                user = user.scalars().first()
                user.image = image
                await session.commit()
                return user
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def update_user(self, new_user: dict):
        async with self.session() as session:
            try:
                statement = select(User).filter(User.id == new_user['id'])
                user = await session.execute(statement)
                user = user.scalars().first()
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
                            if not (user.image is None):
                                user.image = new_user['image']
                        case 'active':
                            user.active = new_user['active']
                        case 'community_patron':
                            community = await community_crud.get_community_by_patron(new_user['community_patron'])
                            user.community_id = community.id
                await session.commit()
                return user
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def delete_user(self, user: User):
        async with self.session() as session:
            try:
                await session.delete(user)
                await session.commit()
                return f"{user} deleted with succesfull"
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def delete_user_by_id(self, user_id: str):
        async with self.session() as session:
            try:
                statement = select(User).filter(User.id == user_id)
                user = await session.execute(statement)
                user = user.scalars().first()
                await session.delete(user)
                await session.commit()
                return f"{user} deleted with succesfull"
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def delete_user_image(self, user_id: str):
        async with self.session() as session:
            try:
                statement = select(User).filter(User.id == user_id)
                user = await session.execute(statement)
                user = user.scalars().first()
                user.image = None
                await session.commit()
                return User
            except Exception as error:
                await session.rollback()
                raise internal_server_error(f"A error occurs during CRUD: {error!r}")
