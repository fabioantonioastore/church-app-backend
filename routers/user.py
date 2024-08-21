from fastapi import APIRouter, status, Depends
from routers.middleware.authorization import verify_user_access_token
from controller.crud.user import UserCrud
from controller.crud.login import LoginCrud
from controller.crud.community import CommunityCrud
from database.session import session
from controller.src.user import (get_user_client_data, get_update_data, is_council_member,
                                 is_parish_leader, upgrade_user_position, convert_user_to_dict)
from schemas.user import UpdateUserModel, UpgradeUserPositionResponsability
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

@router.get('/users/all', status_code=status.HTTP_200_OK, summary="Users", description="Get all users info")
async def get_all_users():
    return await user_crud.get_all_users(session)

@router.get('/me', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)], summary="Users", description="Get user token info")
async def get_user_data(user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(session, user['cpf'])
    return await get_user_client_data(user)

@router.put("/me", status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)], summary="Users", description="Update user info")
async def update_user(user_data: UpdateUserModel, user: dict = Depends(verify_user_access_token)):
    user_data = dict(user_data)
    user_obj = await user_crud.get_user_by_cpf(session, user['cpf'])
    user_data['id'] = user_obj.id
    login = await login_crud.get_login_by_cpf(session, user['cpf'])
    new_login = Login()
    new_login.id = str(uuid4())
    if user_data.get('position'):
        new_login.position = user_data['position']
    else:
        new_login.position = login.position
    if user_data.get('password'):
        new_login.password = hash_pasword(user_data['password'])
    else:
        new_login.password = login.password
    if user_data.get('cpf'):
        new_login.cpf = user_data['cpf']
    else:
        login_update = user_data.copy()
        login_update.pop('cpf')
        login_update['id'] = login.id
        login_update = await login_crud.update_login(session, login_update)
        return {"access_token": jwt.create_access_token(login_update.cpf, login_update.position)}
    await login_crud.delete_login(session, login)
    await user_crud.update_user(session, user_data)
    await login_crud.create_login(session, new_login)
    return {"access_token": jwt.create_access_token(new_login.cpf, new_login.position)}
@router.patch('/user/upgrade/position_and_responsability', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)], summary="Users", description="Upgrade user position")
async def patch_upgrade_user_position(position_data: UpgradeUserPositionResponsability, user: dict = Depends(verify_user_access_token)):
    #if is_parish_leader(user['position']) or is_council_member(user['position']):
    if position_data.position == "user":
        await user_crud.upgrade_user(session, position_data.cpf, position_data.position, "faithful")
        await login_crud.update_position(session, position_data.cpf, position_data.position)
        return
    if position_data.position == "council member":
        if position_data.responsibility:
            await user_crud.upgrade_user(session, position_data.cpf, position_data.position, position_data.responsibility)
            await login_crud.update_position(session, position_data.cpf, position_data.position)
            return
        else:
            await user_crud.upgrade_user(session, position_data.cpf, position_data.position, "member")
            await login_crud.update_position(session, position_data.cpf, position_data.position)
            return
    raise bad_request(f"Rule {position_data.position!r} doesn't exists")
    #raise unauthorized(f"You can't upgrade user position")

@router.delete('/me/deactivate', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)], summary="Users", description="Deactivate user account")
async def deactivate_user_account(user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(session, user['cpf'])
    user.active = False
    user = convert_user_to_dict(user)
    await user_crud.update_user(session, user)
    return {"user account deactivate, do login again to activate"}

@router.get('/users/{cpf}', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)], summary="Users", description="Get user info by CPF")
async def get_user_by_cpf(cpf: str, user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(session, cpf)
    return await get_user_client_data(user)

@router.delete('/users/{cpf}', status_code=status.HTTP_204_NO_CONTENT, summary="Users", description="Delete user by CPF")
async def delete_user_by_cpf(cpf: str):
    login = await login_crud.get_login_by_cpf(session, cpf)
    await login_crud.delete_login(session, login)
    user = await user_crud.get_user_by_cpf(session, cpf)
    await user_crud.delete_user(session, user)