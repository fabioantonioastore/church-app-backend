from sqlalchemy import select
from models import Login
from controller.errors.http.exceptions import not_found
from controller.crud.crud import CRUD


class LoginCrud(CRUD):
    def __init__(self) -> None:
        super().__init__()

    async def update_password(self, cpf: str, password: str):
        async with self.session() as session:
            try:
                statement = select(Login).filter(Login.cpf == cpf)
                login = await session.execute(statement)
                login = login.scalars().first()
                login.password = password
                await session.commit()
                return login
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def update_position(self, cpf: str, position: str):
        async with self.session() as session:
            try:
                statement = select(Login).filter(Login.cpf == cpf)
                login = await session.execute(statement)
                login = login.scalars().first()
                login.position = position
                await session.commit()
                return login
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_login_by_id(self, login_id: str):
        async with self.session() as session:
            try:
                statement = select(Login).filter(Login.id == login_id)
                login = await session.execute(statement)
                return login.scalars().first()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_login_by_cpf(self, login_cpf: str):
        async with self.session() as session:
            try:
                statement = select(Login).filter(Login.cpf == login_cpf)
                login = await session.execute(statement)
                return login.scalars().first()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def create_login(self, login: Login):
        async with self.session() as session:
            try:
                session.add(login)
                await session.commit()
                return login
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def update_login(self, new_login: dict):
        async with self.session() as session:
            try:
                statement = select(Login).filter(Login.id == new_login['id'])
                login = await session.execute(statement)
                login = login.scalars().first()
                for key in new_login.keys():
                    match key:
                        case 'cpf':
                            login.cpf = new_login['cpf']
                        case 'password':
                            login.password = new_login['password']
                        case 'position':
                            login.profile = new_login['position']
                await session.commit()
                return login
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def delete_login(self, login: Login):
        async with self.session() as session:
            try:
                await session.delete(login)
                await session.commit()
                return f"{login} deleted with succesfull"
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def delete_login_by_id(self, login_id: str):
        async with self.session() as session:
            try:
                statement = select(Login).filter(Login.id == login_id)
                login = await session.execute(statement)
                login = login.scalars().first()
                await session.delete(login)
                await session.commit()
                return f"{login} deleted with succesfull"
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")
