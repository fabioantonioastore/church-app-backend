from models.dizimo_payment import DizimoPayment
from models.user import User
from uuid import uuid4
from datetime import datetime

STATUS = ("active", "late", "paid")
MONTHS = (
    "january",
    "february",
    "march",
    "april",
    "nay",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december"
)

def is_valid_payment_status(status: str) -> bool:
    return status in STATUS

def convert_to_month(number: int) -> str:
    return MONTHS[number - 1]

def dizimo_payment_is_paid(payment: DizimoPayment) -> bool:
    return payment.status == "paid"

def complete_dizimo_payment(dizimo_payment: DizimoPayment, pix_payment: dict) -> DizimoPayment:
    dizimo_payment.correlation_id = pix_payment['charge']['correlationID']
    dizimo_payment.status = "active"
    dizimo_payment.value = pix_payment['charge']['value']
    dizimo_payment.date = datetime.now()
    return dizimo_payment

def pass_data_to(dizimo_payment: DizimoPayment, actual_dizimo_payment: DizimoPayment) -> DizimoPayment:
    actual_dizimo_payment.correlation_id = dizimo_payment.correlation_id
    actual_dizimo_payment.status = dizimo_payment.status
    actual_dizimo_payment.date = dizimo_payment.date
    actual_dizimo_payment.value = dizimo_payment.value
    return actual_dizimo_payment

async def create_dizimo_payment(user: User) -> DizimoPayment:
    dizimo_payment = DizimoPayment()
    dizimo_payment.id = str(uuid4())
    dizimo_payment.user_id = user.id
    dizimo_payment.status = "active"
    dizimo_payment.year = datetime.now().year
    dizimo_payment.month = convert_to_month(datetime.now().month)
    return dizimo_payment