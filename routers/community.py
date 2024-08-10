from fastapi import APIRouter, status, Depends
from controller.crud.community import CommunityCrud
from database.session import session
from controller.src.community import (get_patrons, create_community_data, get_community_client_data,
                                      convert_to_dict, update_community_data, get_users_friendly_data,
                                      get_community_list)
from routers.middleware.authorization import verify_user_access_token
from schemas.community import (CreateCommunityModel, UpdateCommunityModel)
from controller.src.user import is_parish_leader, is_council_member
from controller.errors.http.exceptions import unauthorized
from controller.crud.user import UserCrud

router = APIRouter()
community_crud = CommunityCrud()
user_crud = UserCrud()

@router.get('/community/list', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)])
async def communities_list(user: dict = Depends(verify_user_access_token)):
    communities = await community_crud.get_all_communities(session)
    return get_community_list(communities)

@router.get('/patrons', status_code=status.HTTP_200_OK)
async def get_all_patrons():
    communities = await community_crud.get_all_communities(session)
    return get_patrons(communities)

@router.post('/community', status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_user_access_token)])
async def create_community(community: CreateCommunityModel, user: dict = Depends(verify_user_access_token)):
    #if is_parish_leader(user['position']):
    community = create_community_data(dict(community))
    community = await community_crud.create_community(session, community)
    return get_community_client_data(community)
    # raise unauthorized("You can't create the community")

@router.get('/community/{community_patron}', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)])
async def get_community_info(community_patron: str, user: dict = Depends(verify_user_access_token)):
    community = await community_crud.get_community_by_patron(session, community_patron)
    return get_community_client_data(community)

@router.put('/community/{community_patron}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)])
async def update_community(community_patron: str, community_data: UpdateCommunityModel, user: dict = Depends(verify_user_access_token)):
    #if is_parish_leader(user['position']) or is_council_member(user['position']):
    #user = await user_crud.get_user_by_cpf(session, user['cpf'])
    community = await community_crud.get_community_by_patron(session, community_patron)
        #if user.community_id == community.id:
    community_data = dict(community_data)
    await community_crud.update_community(session, update_community_data(community, community_data))
    return {"community updated"}
    #raise unauthorized("You can't update community")
@router.delete('/community/{community_patron}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)])
async def deactivate_community(community_patron: str, user: dict = Depends(verify_user_access_token)):
    #if is_parish_leader(user['position']):
    #user = await user_crud.get_user_by_cpf(session, user['cpf'])
    community = await community_crud.get_community_by_patron(session, community_patron)
        #if user.community_id == community.id:
    community.active = False
    community = convert_to_dict(community)
    await community_crud.update_community(session, community)
    return {"community deactivate"}
    #raise unauthorized("You can't deactivate this community")

@router.get('/community/{community_patron}/users', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)])
async def get_community_users(community_patron: str, user: dict = Depends(verify_user_access_token)):
    #if is_council_member(user['position']) or is_parish_leader(user['position']):
    #user = await user_crud.get_user_by_cpf(session, user['cpf'])
    community = await community_crud.get_community_by_patron(session, community_patron)
        #if user.community_id == community.id:
    return get_users_friendly_data(community.users)
    #raise unauthorized("You can't access this content")

@router.patch('/community/{community_patron}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)])
async def active_community(community_patron: str, user: dict = Depends(verify_user_access_token)):
    #if is_parish_leader(user['position']):
    #user = await user_crud.get_user_by_cpf(session, user['cpf'])
    community = await community_crud.get_community_by_patron(session, community_patron)
        #if user.community_id == community.id:
    community.active = True
    community = convert_to_dict(community)
    await community_crud.update_community(session, community)
    return "community is active now"
    #raise unauthorized("You can't active this community")