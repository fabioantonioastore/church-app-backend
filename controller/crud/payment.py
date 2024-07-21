from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from models.payment import Payment
from controller.errors.http.exceptions import internal_server_error

class PaymentCrud:
    async def get_payment_by_id(self, async_session: async_sessionmaker[AsyncSession], payment_id: str):
        async with async_session() as session:
            try:
                statement = select(Payment).filter(Payment.id == payment_id)
                payment = await session.execute(statement)
                return payment.scalars().one()
            except:
                await session.rollback()
                raise internal_server_error("A error occurs during CRUD")

    async def get_payment_by_user_cpf(self, async_session: async_sessionmaker[AsyncSession], user_cpf: str, total_payments=10):
        async with async_session() as session:
            try:
                statement = select(Payment).filter(Payment.user_cpf == user_cpf)
                payments = await session.execute(statement)
                return payments.scalars().all().count(total_payments)
            except:
                await session.rollback()
                raise internal_server_error("A error occurs during CRUD")

    async def create_payment(self, async_session: async_sessionmaker[AsyncSession], payment: Payment):
        async with async_session() as session:
            try:
                session.add(payment)
                await session.commit()
                return payment
            except:
                await session.rollback()
                raise internal_server_error("A error occurs during CRUD")

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
            except:
                await session.rollback()
                raise internal_server_error("A error occurs during CRUD")

    async def delete_payment(self, async_session: async_sessionmaker[AsyncSession], payment: Payment):
        async with async_session() as session:
            try:
                await session.delete(payment)
                await session.commit()
                return f"{payment} deleted with succesfull"
            except:
                await session.rollback()
                raise internal_server_error("A error occurs during CRUD")

    async def delete_payment_by_id(self, async_session: async_sessionmaker[AsyncSession], payment_id: str):
        async with async_session() as session:
            try:
                statement = select(Payment).filter(Payment.id == payment_id)
                payment = await session.execute(statement)
                payment = payment.scalars().one()
                await session.delete(payment)
                await session.commit()
                return f"{payment} deleted with succesfull"
            except:
                await session.rollback()
                raise internal_server_error("A error occurs during CRUD")