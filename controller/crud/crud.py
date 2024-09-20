from database import session

SESSION = session


class CRUD:
    def __init__(self) -> None:
        self.session = SESSION

    def __repr__(self) -> str:
        return "CRUD()"
