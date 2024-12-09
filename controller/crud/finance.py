from controller.crud.crud import CRUD
from models.finance import Finance
from sqlalchemy import select, and_
from controller.errors.http.exceptions import not_found, internal_server_error
from datetime import datetime
import calendar

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

    async def get_finances_by_year(self, year: int, community_id) -> [Finance]:
        async with self.session() as session:
            try:
                first_month_date = datetime(year, 1, 1)
                last_month_date = datetime(year, 12, calendar.monthrange(year, 12)[1])
                last_month_date = last_month_date.replace(hour=23, minute=59, second=59)
                statement = select(Finance).filter(
                    and_(
                        Finance.community_id == community_id,
                        and_(
                            Finance.date >= first_month_date,
                            Finance.date <= last_month_date
                        )
                    )
                )
                finances = await session.execute(statement)
                return finances.scalars().all()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_finances_by_month(self, year: int, month: int, community_id: str) -> [Finance]:
        async with self.session() as session:
            try:
                first_month_day = datetime(year, month, 1)
                last_month_day = datetime(year, month, calendar.monthrange(year, month)[1])
                last_month_day = last_month_day.replace(hour=23, minute=59, second=59)
                statement = select(Finance).filter(
                    and_(
                        Finance.community_id == community_id,
                        and_(
                            Finance.date >= first_month_day,
                            Finance.date <= last_month_day
                        )
                    )
                )
                finances = await session.execute(statement)
                return finances.scalars().all()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def delete_finance_by_id(self, finance_id: str) -> str:
        async with self.session() as session:
            try:
                statement = select(Finance).filter(Finance.id == finance_id)
                finance = await session.execute(statement)
                finance = finance.scalars().first()
                await session.delete(finance)
                await session.commit()
                return "deleted"
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def update_finance_by_id(self, finance_id: str, finance_data: dict) -> Finance:
        async with self.session() as session:
            try:
                statement = select(Finance).filter(Finance.id == finance_id)
                finance = await session.execute(statement)
                finance = finance.scalars().first()
                for key in finance_data:
                    match key:
                        case "title":
                            finance.title = finance_data['title']
                        case "description":
                            finance.description = finance_data['description']
                        case "type":
                            finance.type = finance_data['type']
                        case "value":
                            finance.value = finance_data['value']
                        case "date":
                            finance.date = finance_data['date']
                await session.commit()
                return finance
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")
