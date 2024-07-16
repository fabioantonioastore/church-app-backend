from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from models.login import Login
from controller.errors.database_error import DatabaseError

class LoginCrud:
    async def get_login_by_id(self, async_session: async_sessionmaker[AsyncSession], login_id: str):
        async with async_session() as session:
            try:
                statement = select(Login).filter(Login.id == login_id)
                login = await session.execute(statement)
                return login.scalars().one()
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def get_login_by_cpf(self, async_session: async_sessionmaker[AsyncSession], login_cpf: str):
        async with async_session() as session:
            try:
                statement = select(Login).filter(Login.cpf == login_cpf)
                login = await session.execute(statement)
                return login.scalars().one()
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def create_login(self, async_session: async_sessionmaker[AsyncSession], login: Login):
        async with async_session() as session:
            try:
                session.add(login)
                await session.commit()
                return login
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def update_login(self, async_session: async_sessionmaker[AsyncSession], new_login: dict):
        async with async_session() as session:
            try:
                statement = select(Login).filter(Login.id == new_login['id'])
                login = await session.execute(statement)
                login = login.scalars().one()
                for key in new_login.keys():
                    match key:
                        case 'password':
                            login.password = new_login['password']
                        case 'profile':
                            login.profile = new_login['profile']
                await session.commit()
                return login
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def delete_login(self, async_session: async_sessionmaker[AsyncSession], login: Login):
        async with async_session() as session:
            try:
                await session.delete(login)
                await session.commit()
                return f"{login} deleted with succesfull"
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def delete_login_by_id(self, async_session: async_sessionmaker[AsyncSession], login_id: str):
        async with async_session() as session:
            try:
                statement = select(Login).filter(Login.id == login_id)
                login = await session.execute(statement)
                login = login.scalars().one()
                await session.delete(login)
                await session.commit()
                return f"{login} deleted with succesfull"
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error