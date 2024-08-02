from fastapi import APIRouter, status, Depends
from controller.crud.community import CommunityCrud
from database.session import session
from controller.src.community import (get_patrons, create_community_data, get_community_client_data,
                                      convert_to_dict, update_community_data)
from routers.middleware.authorization import verify_user_access_token
from schemas.community import (CreateCommunityModel, UpdateCommunityModel)
from controller.src.user import is_parish_leader, is_council_member
from controller.errors.http.exceptions import unauthorized
from controller.crud.user import UserCrud
from controller.auth.cpf_cryptography import get_crypted_cpf

router = APIRouter()
community_crud = CommunityCrud()
user_crud = UserCrud()

@router.get('/patrons', status_code=status.HTTP_200_OK)
async def get_all_patrons():
    communities = await community_crud.get_all_communities(session)
    patrons = get_patrons(communities)
    return patrons

@router.post('/community', status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_user_access_token)])
async def create_community(community: CreateCommunityModel, user: dict = Depends(verify_user_access_token)):
    if is_parish_leader(user['position']):
        community = create_community_data(dict(community))
        community = await community_crud.create_community(session, community)
        return get_community_client_data(community)
    raise unauthorized("You can't create the community")

@router.get('/community/{community_patron}', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)])
async def get_community_info(community_patron: str, user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(session, get_crypted_cpf(user['cpf']))
    community = await community_crud.get_community_by_patron(session, community_patron)
    if user.community_id == community.id:
        return get_community_client_data(community)
    raise unauthorized(f"You can't access this community")

@router.put('/community/{community_patron}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)])
async def update_community(community_patron: str, community_data: UpdateCommunityModel, user: dict = Depends(verify_user_access_token)):
    if is_parish_leader(user['position']) or is_council_member(user['position']):
        user = await user_crud.get_user_by_cpf(session, get_crypted_cpf(user['cpf']))
        community = await community_crud.get_community_by_patron(session, community_patron)
        if user.community_id == community.id:
            community_data = dict(community_data)
            await community_crud.update_community(session, update_community_data(community, community_data))
            return {"community updated"}
    raise unauthorized("You can't update community")
@router.delete('/community/{community_patron}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)])
async def deactivate_community(community_patron: str, user: dict = Depends(verify_user_access_token)):
    if is_parish_leader(user['position']):
        user = await user_crud.get_user_by_cpf(session, get_crypted_cpf(user['cpf']))
        community = await community_crud.get_community_by_patron(session, community_patron)
        if user.community_id == community.id:
            community.active = False
            community = convert_to_dict(community)
            await community_crud.update_community(session, community)
            return {"community deactivate"}
    raise unauthorized("You can't deactivate this community")

@router.patch('/community/{community_patron}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)])
async def active_community(community_patron: str, user: dict = Depends(verify_user_access_token)):
    if is_parish_leader(user['position']):
        user = await user_crud.get_user_by_cpf(session, get_crypted_cpf(user['cpf']))
        community = await community_crud.get_community_by_patron(session, community_patron)
        if user.community_id == community.id:
            community.active = True
            community = convert_to_dict(community)
            await community_crud.update_community(session, community)
            return "community is active now"
    raise unauthorized("You can't active this community")