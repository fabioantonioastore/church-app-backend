from controller.crud.crud import CRUD
from models.finance import Finance
from sqlalchemy import select, and_
from controller.errors.http.exceptions import not_found, internal_server_error


class FinanceCrud(CRUD):
    def __init__(self) -> None:
        super().__init__()

    async def get_all_finances(self) -> [Finance]:
        async with self.session() as session:
            try:
                statement = select(Finance)
                result = await session.execute(statement)
                return result.scalars().all()
            except Exception as error:
                await session.rollback()
                raise internal_server_error(f"A error occurs during CRUD: {error!r}")

    async def create_finance(self, finance: Finance) -> Finance:
        async with self.session() as session:
            try:
                session.add(finance)
                await session.commit()
                return finance
            except Exception as error:
                await session.rollback()
                raise internal_server_error(f"A error occurs during CRUD: {error!r}")

    async def get_finances_by_year(self, year: int, community_id: str = None) -> [Finance]:
        async with self.session() as session:
            try:
                if community_id:
                    statement = select(Finance).filter(
                        and_(
                            Finance.year == year,
                            Finance.community_id == community_id
                        )
                    )
                    result = await session.execute(statement)
                    return result.scalars().all()
                else:
                    statement = select(Finance).filter(Finance.year == year)
                    result = await session.execute(statement)
                    return result.scalars().all()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_finance_by_year_and_month(self, year: int, month: str, community_id: str = None) -> [Finance]:
        async with self.session() as session:
            try:
                if community_id:
                    statement = select(Finance).filter(
                        and_(
                            Finance.year == year,
                            Finance.month == month,
                            Finance.community_id == community_id
                        )
                    )
                    result = await session.execute(statement)
                    return result.scalars().all()
                else:
                    statement = select(Finance).filter(
                        and_(
                            Finance.year == year,
                            Finance.month == month
                        )
                    )
                    result = await session.execute(statement)
                    return result.scalars().all()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")
