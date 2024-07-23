from fastapi import APIRouter, Request, status
from controller.auth import jwt
from controller.crud.user import UserCrud
from database.session import session
from controller.src.user import get_user_client_data

router = APIRouter()
user_crud = UserCrud()

@router.get('/me', status_code=status.HTTP_200_OK)
async def get_user_data(request: Request):
    access_token = request.headers.get("Authorization")
    user = jwt.decode_token(access_token)
    user = await user_crud.get_user_by_cpf(session, user['cpf'])
    user = await get_user_client_data(user)
    return user