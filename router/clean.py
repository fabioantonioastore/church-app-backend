from fastapi import APIRouter
from datetime import datetime

from controller.src.dizimo_payment import convert_to_month
from controller.crud.clean import CleanCRUD
from models.cleaning import Cleaning


clean_crud = CleanCRUD()
router = APIRouter()


@router.post("/clean/{name}/{setor}")
async def clean_post_router(name: str, setor: int):
    clean = Cleaning()
    clean.payed = False
    clean.name = name
    clean.setor = setor
    date = datetime.now()
    clean.year = date.year
    clean.month = convert_to_month(date.month)
    return await clean_crud.create_clean(clean)


@router.put("/clean/{id}")
async def update_clean_payed(id: str):
    return await clean_crud.upgrade_payed(id)


@router.get("/clean/by_setor/{setor}")
async def get_clean_by_setor(setor: int):
    date = datetime.now()
    month = convert_to_month(date.month)
    year = date.year
    return await clean_crud.get_by_setor(setor, month, year)


@router.get("/clean/{month}/{year}")
async def get_clean_by_date(month: str, year: int):
    return await clean_crud.get_by_date(month, year)


@router.get("/clean/test")
async def clean_test():
    return await clean_crud.get_all()


@router.delete("/clean/{id}")
async def clean_delete_router(id: str):
    return await clean_crud.delete_clean(id)
