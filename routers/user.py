from fastapi import APIRouter, status, Depends
from routers.middleware.authorization import verify_user_access_token
from controller.crud.user import UserCrud
from controller.crud.login import LoginCrud
from controller.crud.community import CommunityCrud
from database.session import session
from controller.src.user import (get_user_client_data, get_update_data,
                                 is_parish_leader, upgrade_user_position, convert_user_to_dict)
from schemas.user import UpdateUserModel, UpgradeUserPosition
from controller.errors.http.exceptions import unauthorized, bad_request, internal_server_error
from controller.validators.cpf import CPFValidator
from controller.auth import jwt
from models.login import Login
from uuid import uuid4
from controller.auth.password import hash_pasword

router = APIRouter()
user_crud = UserCrud()
login_crud = LoginCrud()
community_crud = CommunityCrud()

@router.get('/users/all', status_code=status.HTTP_200_OK)
async def get_all_users():
    return await user_crud.get_all_users(session)

@router.get('/me', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)])
async def get_user_data(user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(session, user['cpf'])
    return await get_user_client_data(user)

@router.put("/me", status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)])
async def update_user(user_data: UpdateUserModel, user: dict = Depends(verify_user_access_token)):
    user_data = dict(user_data)
    user = await user_crud.get_user_by_cpf(session, user['cpf'])
    if user_data.get('cpf'):
        CPFValidator(user_data['cpf'])
        cpf = user.cpf
        user = await get_update_data(user, user_data)
        login = await login_crud.get_login_by_cpf(session, cpf)
        await login_crud.delete_login(session, login)
        login.cpf = user['cpf']
        login = Login(
            id = str(uuid4()),
            cpf = login.cpf,
            password = login.password,
            position = login.position
        )
        await user_crud.update_user(session, user)
        await login_crud.create_login(session, login)
    else:
        await user_crud.update_user(session, await get_update_data(user, user_data))
    return {"access_token": jwt.create_access_token(user_data['cpf'], user['position'])}

@router.patch('/user/upgrade/position', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)])
async def patch_upgrade_user_position(position_data: UpgradeUserPosition, user: dict = Depends(verify_user_access_token)):
    if is_parish_leader(user['position']):
        if position_data.position == "user" or position_data.position == "council member":
            user = await user_crud.get_user_by_cpf(session, position_data.cpf)
            login = await login_crud.get_login_by_cpf(session, position_data.cpf)
            data = upgrade_user_position(user, login, position_data.position)
            try:
                await user_crud.update_user(session, data.user)
                try:
                    await login_crud.update_login(session, data.login)
                except Exception as error:
                    raise internal_server_error(f"Database failed to update: {error!r}")
            except Exception as error:
                raise internal_server_error(f"Database failed to update: {error!r}")
            return {"position upgraded"}
        else: raise bad_request(f"Rule {position_data.position} doesn't exist")
    raise unauthorized(f"You can't upgrade user position")

@router.delete('/me/deactivate', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)])
async def deactivate_user_account(user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(session, user['cpf'])
    user.active = False
    user = convert_user_to_dict(user)
    await user_crud.update_user(session, user)
    return {"user account deactivate, do login again to activate"}

@router.get('/users/{cpf}', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)])
async def get_user_by_cpf(cpf: str, user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(session, cpf)
    return await get_user_client_data(user)

@router.delete('/users/{cpf}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)])
async def delete_user_by_cpf(cpf: str, user: dict = Depends(verify_user_access_token)):
    login = await login_crud.get_login_by_cpf(session, cpf)
    await login_crud.delete_login(session, login)
    user = await user_crud.get_user_by_cpf(session, cpf)
    await user_crud.delete_user(session, user)