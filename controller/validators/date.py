from datetime import datetime, date
from controller.errors.date_error import DateError

class DateValidator:
    def __init__(self, date: str):
        self.date = date
        self.is_correct_format()
        self.is_actual_date()

    def is_correct_format(self) -> None:
        try:
            datetime.strptime(self.date, "%Y/%m/%d")
        except DateError as date_error: raise date_error("Invalid format of date, must be \"%Y-%m-%d\"")

    def is_actual_date(self) -> None:
        self.date = datetime.strptime(self.date, "%Y/%m/%d").date()
        today = date.today()
        age = today.year - self.date.year - ((today.month, today.day) < (self.date.month, self.date.day))
        if age > 120: raise DateError("Invalid birthday")