from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from models.dizimo_payment import DizimoPayment
from sqlalchemy import select, and_
from controller.errors.http.exceptions import not_found, internal_server_error
from controller.src.dizimo_payment import is_valid_payment_status

class DizimoPaymentCrud:
    async def get_payment_by_id(self, async_session: async_sessionmaker[AsyncSession], payment_id: str) -> DizimoPayment:
       async with async_session() as session:
           try:
               statement = select(DizimoPayment).filter(DizimoPayment.id == payment_id)
               payment = await session.execute(statement)
               return payment.scalars().one()
           except Exception as error:
               await session.rollback()
               raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_payment_by_correlation_id(self, async_session: async_sessionmaker[AsyncSession], correlation_id: str) -> DizimoPayment:
        async with async_session() as session:
            try:
                statement = select(DizimoPayment).filter(DizimoPayment.correlation_id == correlation_id)
                payment = await session.execute(statement)
                return payment.scalars().one()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_payment_by_identifier(self, async_session: async_sessionmaker[AsyncSession], identifier: str) -> DizimoPayment:
        async with async_session() as session:
            try:
                statement = select(DizimoPayment).filter(DizimoPayment.identifier == identifier)
                payment = await session.execute(statement)
                return payment.scalars().one()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def patch_status(self, async_session: async_sessionmaker[AsyncSession], payment_id: str, status: str) -> DizimoPayment:
        async with async_session() as session:
            try:
                pass
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_payments_by_year(self, async_session: async_sessionmaker[AsyncSession], year: int) -> [DizimoPayment]:
        async with async_session() as session:
            try:
                statement = select(DizimoPayment).filter(DizimoPayment.year == year)
                payments = await session.execute(statement)
                return payments.scalars().all()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_payments_by_month(self, async_session: async_sessionmaker[AsyncSession], month: str) -> [DizimoPayment]:
        async with async_session() as session:
            try:
                statement = select(DizimoPayment).filter(DizimoPayment.month == month)
                payments = await session.execute(statement)
                return payments.scalars().all()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_payments_by_year_and_user_id(self, async_session: async_sessionmaker[AsyncSession], year: int, user_id: str) -> [DizimoPayment]:
        async with async_session() as session:
            try:
                statement = select(DizimoPayment).filter(
                    and_(
                        DizimoPayment.year == year,
                        DizimoPayment.user_id == user_id
                    )
                )
                payments = await session.execute(statement)
                return payments.scalars().all()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_payments_by_month_and_user_id(self, async_session: async_sessionmaker[AsyncSession], month: str, user_id: str) -> [DizimoPayment]:
        async with async_session() as session:
            try:
                statement = select(DizimoPayment).filter(
                    and_(
                        DizimoPayment.month == month,
                        DizimoPayment.user_id == user_id
                    )
                )
                payments = await session.execute(statement)
                return payments.scalars().all()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_payment_by_month_year_and_user_id(self, async_session: async_sessionmaker[AsyncSession], month: str, year: int, user_id: str) -> [DizimoPayment]:
        async with async_session() as session:
            try:
                statement = select(DizimoPayment).filter(
                    and_(DizimoPayment.user_id == user_id,
                         and_(
                             DizimoPayment.month == month,
                             DizimoPayment.year == year
                         ))
                )
                payment = await session.execute(statement)
                return payment.scalars().one()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def create_payment(self, async_session: async_sessionmaker[AsyncSession], payment: DizimoPayment) -> DizimoPayment:
        async with async_session() as session:
            try:
                session.add(payment)
                await session.commit()
                return payment
            except Exception as error:
                await session.rollback()
                raise internal_server_error(f"A error occurs during CRUD: {error!r}")

    async def update_payment(self, async_session: async_sessionmaker[AsyncSession], payment_data: dict) -> DizimoPayment:
        async with async_session() as session:
            try:
                statement = select(DizimoPayment).filter(DizimoPayment.id == payment_data['id'])
                payment = await session.execute(statement)
                payment = payment.scalars().one()
                for key in payment_data.keys():
                    match key:
                        case "status":
                            if is_valid_payment_status(payment_data['status']):
                                payment.status = payment_data['status']
                        case "correlation_id":
                            payment.correlation_id = payment_data['correlation_id']
                        case "value":
                            payment.value = payment_data['value']
                await session.commit()
                return payment
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def delete_payment(self, async_session: async_sessionmaker[AsyncSession], payment: DizimoPayment) -> str:
        async with async_session() as session:
            try:
                await session.delete(payment)
                await session.commit()
                return f"{payment!r}, deleted"
            except Exception as error:
                await session.rollback()
                raise internal_server_error(f"A error occurs during CRUD: {error!r}")

    async def delete_payment_by_id(self, async_session: async_sessionmaker[AsyncSession], payment_id: str) -> str:
        async with async_session() as session:
            try:
                statement = select(DizimoPayment).filter(DizimoPayment.id == payment_id)
                payment = await session.execute(statement)
                payment = payment.scalars().one()
                await session.delete(payment)
                await session.commit()
                return f"{payment!r}, deleted"
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")