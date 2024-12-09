from fastapi import APIRouter, Depends
from router.middleware.authorization import verify_user_access_token
from schemas.finance import CreateFinanceModel
from controller.crud.user import UserCrud
from controller.crud.community import CommunityCrud
from controller.crud.finance import FinanceCrud
from controller.src.finance import create_finance_in_database, finance_no_sensitive_data, month_to_integer

community_crud = CommunityCrud()
user_crud = UserCrud()
finance_crud = FinanceCrud()
router = APIRouter()

@router.post("/community/{community_patron}/finance", dependencies=[Depends(verify_user_access_token)])
async def creaet_finace_obj_router(community_patron: str, finance_data: CreateFinanceModel, user: dict = verify_user_access_token):
    user = await user_crud.get_user_by_cpf(user['cpf'])
    community = await community_crud.get_community_by_patron(community_patron)
    finance_data = dict(finance_data)
    finance_data['community_id'] = community.id
    finance = await create_finance_in_database(finance_data)
    return finance_no_sensitive_data(finance)

@router.get('/community/{community_patron}/finance/{year}', dependencies=[Depends(verify_user_access_token)])
async def get_finance_by_year_router(community_patron: str, year: int, user: dict = verify_user_access_token):
    user = await user_crud.get_user_by_cpf(user['cpf'])
    community = await community_crud.get_community_by_patron(community_patron)
    finances = await finance_crud.get_finances_by_year(year, community.id)
    for finance in finances:
        finance = finance_no_sensitive_data(finance)
    return finances


@router.get('/community/{community_patron}/finance/{year}/{month}', dependencies=Depends(verify_user_access_token))
async def get_finance_by_month_router(community_patron: str, year: int, month: str, user: dict = verify_user_access_token):
    user = await user_crud.get_user_by_cpf(user['cpf'])
    community = await community_crud.get_community_by_patron(community_patron)
    month = month_to_integer(month)
    finances = await finance_crud.get_finances_by_month(year, month, community.id)
    for finance in finances:
        finance = finance_no_sensitive_data(finance)
    return finances
