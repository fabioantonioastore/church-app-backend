from datetime import datetime, date
from controller.errors.http.exceptions import bad_request

class DateValidator:
    def __init__(self, date: str):
        self.date = date
        self.is_correct_format()
        self.is_actual_date()

    def is_correct_format(self) -> None:
        try:
            datetime.strptime(self.date, "%Y-%m-%d")
        except: raise bad_request("Invalid format of date, must be \"%Y-%m-%d\"")

    def is_actual_date(self) -> None:
        self.date = datetime.strptime(self.date, "%Y-%m-%d").date()
        today = date.today()
        age = today.year - self.date.year - ((today.month, today.day) < (self.date.month, self.date.day))
        if age > 120: raise bad_request("Invalid birthday")