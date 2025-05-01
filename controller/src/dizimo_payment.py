from models import DizimoPayment
from models import User
from uuid import uuid4
from datetime import datetime
from controller.src.pix_payment import (
    get_pix_no_sensitive_data,
    get_pix_payment_from_correlation_id,
)

STATUS = ("active", "expired", "paid")
MONTHS = (
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
)

PAID = "paid"
ACTIVE = "active"
EXPIRED = "expired"


def is_valid_payment_status(status: str) -> bool:
    return status in STATUS


def convert_to_month(number: int) -> str:
    return MONTHS[number - 1]


def dizimo_payment_is_paid(payment: DizimoPayment) -> bool:
    return payment.status == PAID


def complete_dizimo_payment(
    dizimo_payment: DizimoPayment, pix_payment: dict
) -> DizimoPayment:
    dizimo_payment.correlation_id = pix_payment["charge"]["correlationID"]
    dizimo_payment.status = ACTIVE
    dizimo_payment.value = pix_payment["charge"]["value"]
    dizimo_payment.date = datetime.now()
    return dizimo_payment


def pass_data_to(
    dizimo_payment: DizimoPayment, actual_dizimo_payment: DizimoPayment
) -> DizimoPayment:
    actual_dizimo_payment.correlation_id = dizimo_payment.correlation_id
    actual_dizimo_payment.status = dizimo_payment.status
    actual_dizimo_payment.date = dizimo_payment.date
    actual_dizimo_payment.value = dizimo_payment.value
    return actual_dizimo_payment


async def create_dizimo_payment(user: User) -> DizimoPayment:
    dizimo_payment = DizimoPayment()
    dizimo_payment.id = str(uuid4())
    dizimo_payment.user_id = user.id
    dizimo_payment.status = ACTIVE
    dizimo_payment.year = datetime.now().year
    dizimo_payment.month = convert_to_month(datetime.now().month)
    return dizimo_payment


def dizimo_payment_is_expired(payment: DizimoPayment) -> bool:
    return payment.status == EXPIRED


def get_dizimo_payment_no_sensitive_data(payment: DizimoPayment) -> dict:
    payment_no_sensitive_data = {
        "status": payment.status,
        "year": payment.year,
        "month": payment.month,
        "payment": None,
    }
    if payment.correlation_id:
        payment_no_sensitive_data["payment"] = get_pix_no_sensitive_data(
            get_pix_payment_from_correlation_id(payment.correlation_id)
        )
    return payment_no_sensitive_data


def get_dizimo_status(dizimo: DizimoPayment) -> str:
    return dizimo.status


async def test_create_dizimo_payment(
    user: User, year: int, month: str
) -> DizimoPayment:
    dizimo_payment = DizimoPayment()
    dizimo_payment.id = str(uuid4())
    dizimo_payment.user_id = user.id
    dizimo_payment.status = ACTIVE
    dizimo_payment.year = year
    dizimo_payment.month = month
    return dizimo_payment


def dizimo_payment_is_active(dizimo: DizimoPayment) -> bool:
    return dizimo.status == ACTIVE
