from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from models.login import Login
from controller.errors.http.exceptions import not_found
from controller.auth.cpf import encrypt, decrypt

class LoginCrud:
    async def update_position(self, async_session: async_sessionmaker[AsyncSession], cpf: str, position: str):
        async with async_session() as session:
            try:
                cpf = encrypt(cpf)
                statement = select(Login).filter(Login.cpf == cpf)
                login = await session.execute(statement)
                login = login.scalars().one()
                login.position = position
                await session.commit()
                login.cpf = decrypt(cpf)
                return login
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_login_by_id(self, async_session: async_sessionmaker[AsyncSession], login_id: str):
        async with async_session() as session:
            try:
                statement = select(Login).filter(Login.id == login_id)
                login = await session.execute(statement)
                login = login.scalars().one()
                login.cpf = decrypt(login.cpf)
                return login
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_login_by_cpf(self, async_session: async_sessionmaker[AsyncSession], login_cpf: str):
        async with async_session() as session:
            try:
                login_cpf = encrypt(login_cpf)
                statement = select(Login).filter(Login.cpf == login_cpf)
                login = await session.execute(statement)
                login = login.scalars().one()
                login.cpf = decrypt(login.cpf)
                return login
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def create_login(self, async_session: async_sessionmaker[AsyncSession], login: Login):
        async with async_session() as session:
            try:
                login.cpf = encrypt(login.cpf)
                session.add(login)
                await session.commit()
                login.cpf = decrypt(login.cpf)
                return login
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def update_login(self, async_session: async_sessionmaker[AsyncSession], new_login: dict):
        async with async_session() as session:
            try:
                if new_login.get('cpf'):
                    new_login['cpf'] = encrypt(new_login['cpf'])
                statement = select(Login).filter(Login.id == new_login['id'])
                login = await session.execute(statement)
                login = login.scalars().one()
                for key in new_login.keys():
                    match key:
                        case 'password':
                            login.password = new_login['password']
                        case 'position':
                            login.profile = new_login['position']
                await session.commit()
                login.cpf = decrypt(login.cpf)
                return login
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def delete_login(self, async_session: async_sessionmaker[AsyncSession], login: Login):
        async with async_session() as session:
            try:
                await session.delete(login)
                await session.commit()
                return f"{login} deleted with succesfull"
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def delete_login_by_id(self, async_session: async_sessionmaker[AsyncSession], login_id: str):
        async with async_session() as session:
            try:
                statement = select(Login).filter(Login.id == login_id)
                login = await session.execute(statement)
                login = login.scalars().one()
                await session.delete(login)
                await session.commit()
                return f"{login} deleted with succesfull"
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")