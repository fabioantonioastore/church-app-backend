from controller.crud.crud import CRUD
from models.number import Number
from sqlalchemy import select
from controller.errors.http.exceptions import not_found, internal_server_error


class NumberCrud(CRUD):
    def __init__(self) -> None:
        super().__init__()

    async def get_number_model_by_number(self, number: str) -> Number:
        async with self.session() as session:
            try:
                statement = select(Number).filter(Number.number == number)
                result = await session.execute(statement)
                number = result.scalars().first()
                return number
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_number_model_by_user_id(self, user_id: str) -> Number:
        async with self.session() as session:
            try:
                statement = select(Number).filter(Number.user_id == user_id)
                result = await session.execute(statement)
                number = result.scalars().first()
                return number
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def update_verification_code(self, number: str, code: int) -> Number:
        async with self.session() as session:
            try:
                statement = select(Number).filter(Number.number == number)
                result = await session.execute(statement)
                number = result.scalars().first()
                number.verification_code = code
                await session.commit()
                return number
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def create_number(self, number: Number) -> Number:
        async with self.session() as session:
            try:
                session.add(number)
                await session.commit()
                return number
            except Exception as error:
                await session.rollback()
                raise internal_server_error(f"A error occurs during CRUD: {error!r}")

    async def update_number_number(self, number: str, new_number: str) -> Number:
        async with self.session() as session:
            try:
                statement = select(Number).filter(Number.number == number)
                result = await session.execute(statement)
                number = result.scalars().first()
                number.number = new_number
                await session.commit()
                return number
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def update_number_by_user_id(self, user_id: str, new_number: str) -> Number:
        async with self.session() as session:
            try:
                statement = select(Number).filter(Number.user_id == user_id)
                result = await session.execute(statement)
                number = result.scalars().first()
                number.number = new_number
                await session.commit()
                return number
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")
