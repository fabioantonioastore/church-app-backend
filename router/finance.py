from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from router.middleware.authorization import verify_user_access_token
from schemas.finance import CreateFinanceModel, UpdateFinanceModel, DictCreateFinanceModel
from controller.crud.user import UserCrud
from controller.crud.community import CommunityCrud
from controller.crud.finance import FinanceCrud
from controller.src.finance import (create_finance_in_database, finance_no_sensitive_data, month_to_integer,
                                    get_total_available_money_from_finances_obj, create_finance_model,
                                    is_actual_month_and_year, update_finance_months_by_finance_data,
                                    FinanceData, FinanceType, get_finance_resume, get_csv_finance_resume,
                                    DateYearMonth, integer_to_month)

community_crud = CommunityCrud()
user_crud = UserCrud()
finance_crud = FinanceCrud()
router = APIRouter()

@router.post("/community/{community_patron}/finance", status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_user_access_token)])
async def create_finance_obj_router(community_patron: str, finance_data: CreateFinanceModel | DictCreateFinanceModel, user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(user['cpf'])
    community = await community_crud.get_community_by_patron(community_patron)
    if isinstance(finance_data, CreateFinanceModel):
        finance_data = dict(finance_data)
        finance_data['community_id'] = community.id
        finance = await create_finance_in_database(finance_data)
        return finance_no_sensitive_data(finance)
    elif isinstance(finance_data, DictCreateFinanceModel):
        finance_data = dict(finance_data)
        finance_objs = []
        for key in finance_data.keys():
            finance = finance_data[key]
            finance['community_id'] = community.id
            finance = create_finance_model(finance)
            finance_objs.append(finance)
        finance_models = []
        for finance in finance_objs:
            finance = await finance_crud.create_finance(finance)
            finance_models.append(finance)
        return finance_models

@router.get('/community/{community_patron}/finance/{year}', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)])
async def get_finance_by_year_router(community_patron: str, year: int, user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(user['cpf'])
    community = await community_crud.get_community_by_patron(community_patron)
    finances = await finance_crud.get_finances_by_year(year, community.id)
    finances = [finance_no_sensitive_data(finance) for finance in finances]
    return {"finances": finances, "total": get_total_available_money_from_finances_obj(finances)}


@router.get('/community/{community_patron}/finance/{year}/{month}', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)])
async def get_finance_by_month_router(community_patron: str, year: int, month: str, user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(user['cpf'])
    community = await community_crud.get_community_by_patron(community_patron)
    month = month_to_integer(month)
    finances = await finance_crud.get_finances_by_month(year, month, community.id)
    finances = [finance_no_sensitive_data(finance) for finance in finances]
    return {"finances": finances, "total": get_total_available_money_from_finances_obj(finances)}

@router.delete('/community/{community_patron}/finance/{id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)])
async def delete_finance_by_id_router(community_patron: str, id: str, user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(user['cpf'])
    community = await community_crud.get_community_by_patron(community_patron)
    finance = await finance_crud.get_finance_by_id(id)
    await finance_crud.delete_finance_by_id(id)
    if is_actual_month_and_year(finance):
        return
    if finance.type == FinanceType.INPUT:
        finance_data = FinanceData(value=finance.value, type=FinanceType.OUTPUT, date=finance.date)
        await update_finance_months_by_finance_data(finance_data)
    elif finance.type == FinanceType.OUTPUT:
        finance_data = FinanceData(value=finance.value, type=FinanceType.INPUT, date=finance.date)
        await update_finance_months_by_finance_data(finance_data)
    return

@router.put('/community/{community_patron}/finance/{id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)])
async def update_finance_by_id(community_patron: str, id: str, finance_data: UpdateFinanceModel, user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(user['cpf'])
    community = await community_crud.get_community_by_patron(community_patron)
    last_finance = await finance_crud.get_finance_by_id(id)
    finance_data = dict(finance_data)
    finance = await finance_crud.update_finance_by_id(id, finance_data)
    if not (is_actual_month_and_year(finance)):
        abs_value = abs(finance_data['value'] - finance.value)
        finance_dataclass = FinanceData(value=abs_value, type=finance.type, date=last_finance.date)
        if not (
            finance_dataclass.value == 0 and
            finance_dataclass.type == last_finance.type
        ):
            await update_finance_months_by_finance_data(finance_dataclass)
    return finance_no_sensitive_data(finance)

@router.get('/community/{patron}/finance_resume/{year}', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)])
async def get_finance_resume_by_year(patron: str, year: int, user: dict = Depends(verify_user_access_token)):
    community = await community_crud.get_community_by_patron(patron)
    finance_resume = {}
    for i in range(1, 13):
        month = integer_to_month(i)
        try:
            finances = await finance_crud.get_finances_by_month(year, i, community.id)
            finance_resume[month] = get_finance_resume(finances)
        except:
            finance_resume[month] = None
    return finance_resume


@router.get('/community/{patron}/finance_resume/{year}/{month}', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)])
async def get_finance_resume_by_year_and_month(patron: str, year: int, month: str, user: dict = Depends(verify_user_access_token)):
    community = await community_crud.get_community_by_patron(patron)
    month = month_to_integer(month)
    finances = await finance_crud.get_finances_by_month(year, month, community.id)
    month = integer_to_month(month)
    resume = get_finance_resume(finances)
    return {month: resume}

@router.get('/community/{patron}/finance_resume_csv/{year}/{month}', status_code=status.HTTP_200_OK)
async def get_finance_resume_csv_by_year_and_month(patron: str, year: int, month: str):
    community = await community_crud.get_community_by_patron(patron)
    month = month_to_integer(month)
    finances = await finance_crud.get_finances_by_month(year, month, community.id)
    csv_file = await get_csv_finance_resume(finances)
    response = StreamingResponse(
        iter([csv_file.getvalue()]),
        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = "attachment; filename=finance_resume.csv"
    return response