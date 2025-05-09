from datetime import datetime
from controller.crud.clean import CleanCRUD
from models.cleaning import Cleaning
from controller.src.dizimo_payment import convert_to_month
from typing import NamedTuple
from asyncio import run


class NameAndSetor(NamedTuple):
    name: str
    setor: int


clean_crud = CleanCRUD()


async def create_new_cleaning():
    date = datetime.now()
    month = date.month
    month_get = month - 1
    year = date.year
    if month == 1:
        year = year - 1
        month_get = 12
    month = convert_to_month(month)
    month_get = convert_to_month(month_get)

    info = []
    cleans = await clean_crud.get_by_date(month_get, year)
    for clean in cleans:
        clean_data = NameAndSetor(clean.name, clean.setor)
        info.append(clean_data)

    for i in info:
        clean = Cleaning()
        clean.name = i.name
        clean.setor = i.setor
        clean.month = month
        clean.year = date.year
        clean.payed = False
        await clean_crud.create_clean(clean)
