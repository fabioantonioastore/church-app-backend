from typing import NoReturn
from controller.crud.dizimo_payment import DizimoPaymentCrud
from database.session import session
from controller.src.pix_payment import get_pix_payment_from_correlation_id
from controller.src.pix_payment import is_pix_paid
from controller.src.pix_payment import delete_pix_by_correlation_id, get_pix_value
from models.user import User
from controller.crud.user import UserCrud
from controller.crud.community import CommunityCrud

dizimo_payment_crud = DizimoPaymentCrud()
user_crud = UserCrud()
community_crud = CommunityCrud()

async def update_payment_db(correlation_id: str, user: User = None) -> NoReturn:
    dizimo_payment = await dizimo_payment_crud.get_payment_by_correlation_id(session, correlation_id)
    pix_payment = get_pix_payment_from_correlation_id(dizimo_payment.correlation_id)
    if is_pix_paid(pix_payment):
        await dizimo_payment_crud.update_status(session, dizimo_payment.id, "PAID")
        if not(user):
            user = await user_crud.get_user_by_id(session, dizimo_payment.user_id)
        await community_crud.increase_actual_month_payment_value(session, user.community_id, get_pix_value(pix_payment))
        return
    delete_pix_by_correlation_id(dizimo_payment.correlation_id)
    await dizimo_payment_crud.update_correlation_id_to_none(session, dizimo_payment.id)