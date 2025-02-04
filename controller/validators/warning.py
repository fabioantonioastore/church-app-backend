from controller.errors.http.exceptions import bad_request
from typing import NoReturn


class WarningValidator:
    def __init__(self, warning_data: dict) -> NoReturn:
        self.warning_data = warning_data

    def validate_scope(self) -> NoReturn:
        scope = self.warning_data["scope"]
        if scope != "public" or scope != "private":
            raise bad_request(
                f"Invalid scope {scope}, scope must be public or private"
            )
