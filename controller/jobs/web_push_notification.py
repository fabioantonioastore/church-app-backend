from datetime import datetime
from controller.crud.dizimo_payment import DizimoPaymentCrud
from controller.src.dizimo_payment import (
    convert_to_month,
    dizimo_payment_is_active,
)
from firebase_admin import messaging
from typing import NoReturn

dizimo_payment_crud = DizimoPaymentCrud()


def execute_notification(token: str, title: str, body: str) -> NoReturn:
    try:
        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            token=token,
        )
        messaging.send(message)
    except Exception as error:
        print(error)


async def send_notification() -> NoReturn:
    try:
        from controller.src.web_push_notification import (
            get_web_pushes,
            is_first_month_day,
        )

        web_pushes = await get_web_pushes()
        for web_push in web_pushes:
            user = web_push.user
            token = web_push.token
            month = convert_to_month(datetime.month)
            year = datetime.year
            day = datetime.day
            dizimo = await dizimo_payment_crud.get_payment_by_month_year_and_user_id(
                month, year, user.id
            )
            if is_first_month_day(day):
                title = f"E-Igreja"
                body = f"Pagamento de {month} ja disponivel"
                execute_notification(token, title, body)
                return
            if dizimo_payment_is_active(dizimo):
                title = f"E-Igreja"
                body = f"Pagamento de {month} ainda pendente"
                execute_notification(token, title, body)
                return
            title = f"E-Igreja"
            body = (
                f"Convide amigos para fazer parte! Agradecemos pela sua contribuicao!"
            )
            execute_notification(token, title, body)
    except:
        pass
