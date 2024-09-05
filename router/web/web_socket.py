from fastapi import APIRouter, WebSocket, Depends
from router.middleware.authorization import verify_user_access_token
from controller.crud.user import UserCrud
import time
from controller.crud.dizimo_payment import DizimoPaymentCrud
from controller.src.pix_payment import get_pix_payment_from_correlation_id, is_pix_active, is_pix_expired, is_pix_paid
from datetime import datetime
from controller.errors.http.exceptions import internal_server_error
from asyncio import sleep

router = APIRouter()
user_crud = UserCrud()
dizimo_crud = DizimoPaymentCrud()

ACTIVE = "ACTIVE"
EXPIRED = "EXPIRED"
PAID = "PAID"


@router.websocket("/ws/verify_payment_pix/{year}/{month}", dependencies=[Depends(verify_user_access_token)])
async def verify_user_pix_payment(websocket: WebSocket, year: int, month: str,
                                  user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(user["cpf"])
    dizimo = await dizimo_crud.get_payment_by_month_year_and_user_id(month, year, user.id)
    correlation_id = dizimo.correlation_id
    max_duration = 60 * 30
    verification_time = 60
    start_time = time.time()
    while True:
        try:
            pix_payment = get_pix_payment_from_correlation_id(correlation_id)
            if is_pix_active(pix_payment):
                await websocket.send_json(
                    {
                        "status": ACTIVE,
                        "date": datetime.now().isoformat()
                    }
                )
                if time.time() - start_time >= max_duration:
                    break
            if is_pix_expired(pix_payment):
                await websocket.send_json(
                    {
                        "status": EXPIRED,
                        "date": datetime.now().isoformat()
                    }
                )
                break
            if is_pix_paid(pix_payment):
                await websocket.send_json(
                    {
                        "status": PAID,
                        "date": datetime.now().isoformat()
                    }
                )
                break
            await sleep(verification_time)
        except Exception as error:
            raise internal_server_error(str(error))
    await websocket.close()
