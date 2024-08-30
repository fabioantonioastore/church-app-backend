from fastapi import APIRouter, Depends, status
from models.dizimo_payment import DizimoPayment
from controller.crud.dizimo_payment import DizimoPaymentCrud
from controller.auth import jwt
from routers.middleware.authorization import verify_user_access_token
from controller.crud.user import UserCrud
from database.session import session
from datetime import datetime
from uuid import uuid4
from controller.src.dizimo_payment import convert_to_month, dizimo_payment_is_paid, complete_dizimo_payment
from controller.errors.http.exceptions import bad_request
from controller.src.pix_payment import PixPayment, create_customer, make_post_pix_request, get_pix_no_sensitive_data
from schemas.dizimo_payment import CreateDizimoPaymentModel

router = APIRouter()
dizimo_payment_crud = DizimoPaymentCrud()
user_crud = UserCrud()

@router.post("/dizimo_payment", status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_user_access_token)])
async def create_dizimo_payment_router(pix_data: CreateDizimoPaymentModel, user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(session, user['cpf'])
    pix_data = dict(pix_data)
    month = pix_data['month']
    year = pix_data['year']
    dizimo_payment = await dizimo_payment_crud.get_payment_by_month_year_and_user_id(session, month, year, user.id)
    if dizimo_payment_is_paid(dizimo_payment):
        raise bad_request(f"Payment already paid")
    pix_payment = PixPayment(
        value = pix_data['value'],
        customer = create_customer(user),
        correlationID = str(uuid4())
    )
    pix_payment = make_post_pix_request(pix_payment)
    dizimo_payment = complete_dizimo_payment(dizimo_payment, pix_payment)
    await dizimo_payment_crud.complete_dizimo_payment(session, dizimo_payment)
    return get_pix_no_sensitive_data(pix_payment)