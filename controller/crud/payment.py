from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from models.payment import Payment
from controller.errors.http.exceptions import not_found

class PaymentCrud:
    async def get_payment_by_id(self, async_session: async_sessionmaker[AsyncSession], payment_id: str):
        async with async_session() as session:
            try:
                statement = select(Payment).filter(Payment.id == payment_id)
                payment = await session.execute(statement)
                return payment.scalars().one()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_payment_by_user_cpf(self, async_session: async_sessionmaker[AsyncSession], user_cpf: str, total_payments=10):
        async with async_session() as session:
            try:
                statement = select(Payment).filter(Payment.user_cpf == user_cpf)
                payments = await session.execute(statement)
                return payments.scalars().all().count(total_payments)
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def create_payment(self, async_session: async_sessionmaker[AsyncSession], payment: Payment):
        async with async_session() as session:
            try:
                session.add(payment)
                await session.commit()
                return payment
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def update_payment(self, async_session: async_sessionmaker[AsyncSession], new_payment: dict):
        async with async_session() as session:
            try:
                statement = select(Payment).filter(Payment.id == new_payment['id'])
                payment = await session.execute(statement)
                payment = payment.scalars().one()
                for key in new_payment.keys():
                    match key:
                        case 'date':
                            payment.date = new_payment['date']
                        case 'value':
                            payment.value = new_payment['value']
                        case 'type':
                            payment.type = new_payment['type']
                        case 'status':
                            payment.status = new_payment['status']
                await session.commit()
                return payment
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def delete_payment(self, async_session: async_sessionmaker[AsyncSession], payment: Payment):
        async with async_session() as session:
            try:
                await session.delete(payment)
                await session.commit()
                return f"{payment} deleted with succesfull"
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def delete_payment_by_id(self, async_session: async_sessionmaker[AsyncSession], payment_id: str):
        async with async_session() as session:
            try:
                statement = select(Payment).filter(Payment.id == payment_id)
                payment = await session.execute(statement)
                payment = payment.scalars().one()
                await session.delete(payment)
                await session.commit()
                return f"{payment} deleted with succesfull"
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")