from fastapi import APIRouter, status, Depends
from router.middleware.authorization import verify_user_access_token
from controller.crud import CommunityCrud, NumberCrud, UserCrud, LoginCrud
from controller.src.user import (
    get_user_client_data,
    get_update_data,
    is_council_member,
    is_parish_leader,
    upgrade_user_position,
    convert_user_to_dict,
)
from schemas.user import UpdateUserModel, UpgradeUserPositionResponsability
from controller.errors.http.exceptions import (
    unauthorized,
    bad_request,
    internal_server_error,
)
from controller.validators.cpf import CPFValidator
from controller.auth import jwt
from models import Login
from uuid import uuid4
from controller.auth.password import hash_pasword
from datetime import datetime
from controller.validators.phone import PhoneValidator
from io import BytesIO

router = APIRouter()
user_crud = UserCrud()
login_crud = LoginCrud()
community_crud = CommunityCrud()
number_crud = NumberCrud()


@router.get(
    "/users/all",
    status_code=status.HTTP_200_OK,
    summary="Users",
    description="Get all users info",
)
async def get_all_users():
    users = await user_crud.get_all_users()
    for user in users:
        community = await community_crud.get_community_by_id(user.community_id)
        user.community_id = community.patron
    return users


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_user_access_token)],
    summary="Users",
    description="Get user token info",
)
async def get_user_data(user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(user["cpf"])
    return await get_user_client_data(user)


@router.put(
    "/me",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_user_access_token)],
    summary="Users",
    description="Update user info",
)
async def update_user(
    user_data: UpdateUserModel, user: dict = Depends(verify_user_access_token)
):
    user_data = dict(user_data)
    CPFValidator(user_data["cpf"])
    user = await user_crud.get_user_by_cpf(user["cpf"])
    if user_data.get("phone"):
        PhoneValidator(user_data["phone"])
        await number_crud.update_number_by_user_id(user.id, user_data["phone"])
    user_data["id"] = user.id
    if user_data["birthday"]:
        user_data["birthday"] = datetime.strptime(user_data["birthday"], "%Y-%m-%d")
    login = await login_crud.get_login_by_cpf(user.cpf)
    await login_crud.delete_login(login)
    try:
        user = await user_crud.update_user(user_data)
    except Exception as error:
        login_obj = Login()
        login_obj.id = str(uuid4())
        login_obj.position = login.position
        login_obj.cpf = login.cpf
        login_obj.password = login.password
        await login_crud.create_login(login_obj)
        raise bad_request(f"This data is already in use: {error!r}")
    new_login = Login(id=str(uuid4()), position=user.position, cpf=user.cpf)
    if user_data.get("password"):
        if not (user_data["password"] is None):
            new_login.password = hash_pasword(user_data["password"])
        else:
            new_login.password = login.password
    else:
        new_login.password = login.password
    await login_crud.create_login(new_login)
    return {"access_token": jwt.create_access_token(user.cpf, user.position)}


@router.patch(
    "/user/upgrade/position_and_responsability",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_user_access_token)],
    summary="Users",
    description="Upgrade user position",
)
async def patch_upgrade_user_position(
    position_data: UpgradeUserPositionResponsability,
    user: dict = Depends(verify_user_access_token),
):
    # if is_parish_leader(user['position']) or is_council_member(user['position']):
    if position_data.position == "user":
        await user_crud.upgrade_user(
            position_data.cpf, position_data.position, "faithful"
        )
        await login_crud.update_position(position_data.cpf, positigon_data.position)
        return
    if position_data.position == "council member":
        if position_data.responsibility:
            await user_crud.upgrade_user(
                position_data.cpf,
                position_data.position,
                position_data.responsibility,
            )
            await login_crud.update_position(position_data.cpf, position_data.position)
            return
        else:
            await user_crud.upgrade_user(
                position_data.cpf, position_data.position, "member"
            )
            await login_crud.update_position(position_data.cpf, position_data.position)
            return
    raise bad_request(f"Rule {position_data.position!r} doesn't exists")
    # raise unauthorized(f"You can't upgrade user position")


@router.delete(
    "/me/deactivate",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_user_access_token)],
    summary="Users",
    description="Deactivate user account",
)
async def deactivate_user_account(
    user: dict = Depends(verify_user_access_token),
):
    user = await user_crud.get_user_by_cpf(user["cpf"])
    user.active = False
    user = convert_user_to_dict(user)
    await user_crud.update_user(user)
    return {"user account deactivate, do login again to activate"}


@router.get(
    "/users/{cpf}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_user_access_token)],
    summary="Users",
    description="Get user info by CPF",
)
async def get_user_by_cpf(cpf: str, user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(cpf)
    return await get_user_client_data(user)


@router.delete(
    "/users/{cpf}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Users",
    description="Delete user by CPF",
)
async def delete_user_by_cpf(cpf: str):
    login = await login_crud.get_login_by_cpf(cpf)
    await login_crud.delete_login(login)
    user = await user_crud.get_user_by_cpf(cpf)
    await user_crud.delete_user(user)
