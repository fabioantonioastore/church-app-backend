from sqlalchemy import select, and_

from models import WarningView, User
from controller.crud import CRUD

class WarningViewCRUD(CRUD):
    def __init__(self) -> None:
        super().__init__()

    async def get_warnings_view_by_warning_id(self, warning_id: str) -> list[WarningView]:
        async with self.session() as session:
            try:
                statement = select(WarningView).filter(WarningView.warning_id == warning_id)
                result = await session.execute(statement)

                return result.scalars().all()
            except Exception as error:
                await session.rollback()
                raise error

    async def get_warning_view_by_cpf_and_warning_id(self, cpf: str, warning_id: str) -> WarningView:
        async with self.session() as session:
            try:
                statement = (
                    select(WarningView)
                    .filter(
                        and_(
                            WarningView.cpf == cpf,
                            WarningView.warning_id == warning_id
                        )
                    )
                )
                result = await session.execute(statement)
                return result.scalars().one()
            except Exception as error:
                await session.rollback()
                raise error

    async def update_warnings_view_cpf(self, cpf: str, new_cpf: str) -> list[WarningView]:
        async with self.session() as session:
            try:
                statement = select(WarningView).filter(WarningView.cpf == cpf)
                result = await session.execute(statement)
                warnings_view = result.scalars().all()

                for warning_view in warnings_view:
                    warning_view.cpf = new_cpf
                    session.add(warning_view)

                await session.commit()
                return  warnings_view
            except Exception as error:
                await session.rollback()
                raise error

    async def delete_warnings_view_by_cpf(self, cpf: str) -> None:
        async with self.session() as session:
            try:
                statement = select(WarningView).filter(WarningView.cpf == cpf)
                result = await session.execute(statement)
                warnings_view = result.scalars().all()

                for warning_view in warnings_view:
                    await session.delete(warning_view)

                await session.commit()
            except Exception as error:
                await session.rollback()
                raise error

    async def get_warning_view_by_cpf(self, cpf: str) -> WarningView:
        async with self.session() as session:
            try:
                statement = select(WarningView).filter(WarningView.cpf == cpf)
                result = await session.execute(statement)

                return result.scalars().all()
            except Exception as error:
                await session.rollback()
                raise error

    async def create_warning_view(self, warning_view: WarningView) -> WarningView:
        async with self.session() as session:
            try:
                session.add(warning_view)
                await session.commit()

                return warning_view
            except Exception as error:
                await session.rollback()
                raise error

    async def delete_warnings_view_by_warning_id(self, warning_id: str) -> None:
        async with self.session() as session:
            try:
                warnings_view = await self.get_warnings_view_by_warning_id(warning_id)
                for warning_view in warnings_view:
                    await session.delete(warning_view)

                await session.commit()
            except Exception as error:
                await session.rollback()
                raise error
