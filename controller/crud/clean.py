from controller.crud.crud import CRUD
from models.cleaning import Cleaning

from sqlalchemy import select, and_


class CleanCRUD(CRUD):
    def __init__(self) -> None:
        super().__init__()

    async def get_all(self) -> list[Cleaning]:
        async with self.session() as session:
            statement = select(Cleaning)
            result = await session.execute(statement)
            return result.scalars().all()

    async def create_clean(self, clean_model: Cleaning) -> Cleaning:
        async with self.session() as session:
            session.add(clean_model)
            await session.commit()
            return clean_model

    async def get_by_setor(self, setor: int, month: str, year: int) -> list[Cleaning]:
        async with self.session() as session:
            statement = select(Cleaning).filter(
                and_(
                    and_(Cleaning.year == year, Cleaning.month == month),
                    Cleaning.setor == setor,
                )
            )
            result = await session.execute(statement)
            return result.scalars().all()

    async def get_by_date(self, month: str, year: int) -> list[Cleaning]:
        async with self.session() as session:
            statement = select(Cleaning).filter(
                and_(Cleaning.year == year, Cleaning.month == month)
            )
            result = await session.execute(statement)
            return result.scalars().all()

    async def upgrade_payed(self, id: str, value: int) -> Cleaning:
        async with self.session() as session:
            statement = select(Cleaning).filter(Cleaning.id == id)
            result = await session.execute(statement)
            clean = result.scalars().one()
            clean.value = value
            session.add(clean)
            await session.commit()
            return clean


    async def delete_all(self) -> str:
        async with self.session() as session:
            statement = select(Cleaning)
            result = await session.execute(statement)
            cleaners = result.scalars().all()
            for cleaner in cleaners:
                await session.delete(cleaner)
            await session.commit()
            return "deleted"

    async def delete_by_id(self, id: str) -> str:
        async with self.session() as session:
            statement = select(Cleaning).filter(Cleaning.id == id)
            result = await session.execute(statement)
            cleaner = result.scalars().first()
            await session.delete(cleaner)
            await session.commit()
            return "deleted"