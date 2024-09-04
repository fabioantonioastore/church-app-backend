from models.dizimo_payment import DizimoPayment
from sqlalchemy import select, and_
from typing import AsyncIterator
from controller.errors.http.exceptions import not_found, internal_server_error
from controller.src.dizimo_payment import is_valid_payment_status
from controller.src.dizimo_payment import pass_data_to
from database.session import session as db_session

SESSION = db_session


class DizimoPaymentCrud:
    def __init__(self) -> None:
        self.session = SESSION

    async def get_all(self):
        async with self.session() as session:
            try:
                statement = select(DizimoPayment)
                payments = await session.execute(statement)
                return payments.scalars().all()
            except Exception as error:
                await session.rollback()
                raise internal_server_error(f"A error occurs during CRUD")

    async def get_all_user_dizimo_payment(self, user_id: str, page: int = 1, page_size: int = 100) -> AsyncIterator:
        async with self.session() as session:
            try:
                offset = (page - 1) * page_size
                statement = select(DizimoPayment).filter(DizimoPayment.user_id == user_id).offset(offset).limit(
                    page_size)
                dizimo_payments = await session.execute(statement)
                dizimo_payments = dizimo_payments.scalars().all()
                yield dizimo_payments
            except Exception as error:
                await session.rollback()
                raise internal_server_error(f"A error occurs during CRUD: {error!r}")

    async def get_payment_by_id(self, payment_id: str) -> DizimoPayment:
        async with self.session() as session:
            try:
                statement = select(DizimoPayment).filter(DizimoPayment.id == payment_id)
                payment = await session.execute(statement)
                return payment.scalars().one()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_payment_by_correlation_id(self, correlation_id: str) -> DizimoPayment:
        async with self.session() as session:
            try:
                statement = select(DizimoPayment).filter(DizimoPayment.correlation_id == correlation_id)
                payment = await session.execute(statement)
                return payment.scalars().one()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_payment_by_identifier(self, identifier: str) -> DizimoPayment:
        async with self.session() as session:
            try:
                statement = select(DizimoPayment).filter(DizimoPayment.identifier == identifier)
                payment = await session.execute(statement)
                return payment.scalars().one()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_payments_by_year(self, year: int) -> [DizimoPayment]:
        async with self.session() as session:
            try:
                statement = select(DizimoPayment).filter(DizimoPayment.year == year)
                payments = await session.execute(statement)
                return payments.scalars().all()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_payments_by_month(self, month: str) -> [DizimoPayment]:
        async with self.session() as session:
            try:
                statement = select(DizimoPayment).filter(DizimoPayment.month == month)
                payments = await session.execute(statement)
                return payments.scalars().all()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_payments_by_year_and_user_id(self, year: int, user_id: str) -> [DizimoPayment]:
        async with self.session() as session:
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

    async def get_payments_by_month_and_user_id(self, month: str, user_id: str) -> [DizimoPayment]:
        async with self.session() as session:
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

    async def get_payment_by_month_year_and_user_id(self, month: str, year: int, user_id: str) -> [DizimoPayment]:
        async with self.session() as session:
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

    async def create_payment(self, payment: DizimoPayment) -> DizimoPayment:
        async with self.session() as session:
            try:
                session.add(payment)
                await session.commit()
                return payment
            except Exception as error:
                await session.rollback()
                raise internal_server_error(f"A error occurs during CRUD: {error!r}")

    async def update_payment(self, payment_data: dict) -> DizimoPayment:
        async with self.session() as session:
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
                        case "identifier":
                            payment.identifier = payment_data['identifier']
                await session.commit()
                return payment
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def complete_dizimo_payment(self, dizimo_payment: DizimoPayment) -> DizimoPayment:
        async with self.session() as session:
            try:
                statement = select(DizimoPayment).filter(DizimoPayment.id == dizimo_payment.id)
                actual_dizimo_payment = await session.execute(statement)
                actual_dizimo_payment = actual_dizimo_payment.scalars().one()
                actual_dizimo_payment = pass_data_to(dizimo_payment, actual_dizimo_payment)
                await session.commit()
                return actual_dizimo_payment
            except Exception as error:
                await session.rollback()
                raise internal_server_error(f"A error occurs during CRUD: {error!r}")

    async def delete_payment(self, payment: DizimoPayment) -> str:
        async with self.session() as session:
            try:
                await session.delete(payment)
                await session.commit()
                return f"{payment!r}, deleted"
            except Exception as error:
                await session.rollback()
                raise internal_server_error(f"A error occurs during CRUD: {error!r}")

    async def delete_payment_by_id(self, payment_id: str) -> str:
        async with self.session() as session:
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

    async def update_status(self, dizimo_payment_id: str, status: str) -> DizimoPayment:
        async with self.session() as session:
            try:
                statement = select(DizimoPayment).filter(DizimoPayment.id == dizimo_payment_id)
                payment = await session.execute(statement)
                payment = payment.scalars().one()
                if is_valid_payment_status(status):
                    payment.status = status
                    await session.commit()
                    return payment
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def update_correlation_id(self, dizimo_payment_id: str, correlation_id: str = None) -> DizimoPayment:
        async with self.session() as session:
            try:
                statement = select(DizimoPayment).filter(DizimoPayment.id == dizimo_payment_id)
                payment = await session.execute(statement)
                payment = payment.scalars().one()
                payment.correlation_id = correlation_id
                await session.commit()
                return payment
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def update_correlation_id_to_none(self, dizimo_payment_id: str) -> DizimoPayment:
        async with self.session() as session:
            try:
                statement = select(DizimoPayment).filter(DizimoPayment.id == dizimo_payment_id)
                payment = await session.execute(statement)
                payment = payment.scalars().one()
                payment.correlation_id = None
                payment.value = None
                payment.date = None
                await session.commit()
                return payment
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")
