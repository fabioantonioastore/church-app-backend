from fastapi import APIRouter, Request, status, Depends
from routers.middleware.authorization import verify_user_access_token
from controller.crud.user import UserCrud
from database.session import session
from controller.src.user import get_user_client_data
from controller.auth.cpf_cryptography import get_crypted_cpf

router = APIRouter()
user_crud = UserCrud()

@router.get('/me', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)])
async def get_user_data(user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(session, get_crypted_cpf(user['cpf']))
    user = await get_user_client_data(user)
    return user