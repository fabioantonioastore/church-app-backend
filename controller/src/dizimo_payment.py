STATUS = ("ACTIVE", "LATE", "PAID")

def is_valid_payment_status(status: str) -> bool:
    return status in STATUS