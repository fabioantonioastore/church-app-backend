from fastapi import APIRouter, status, Depends
from controller.crud.community import CommunityCrud
from database.session import session
from controller.src.community import get_patrons
from routers.middleware.authorization import verify_user_access_token
from schemas.community import CreateCommunityModel

router = APIRouter()
community_crud = CommunityCrud()

@router.get('/patrons', status_code=status.HTTP_200_OK)
async def get_all_patrons():
    communities = await community_crud.get_all_communities(session)
    patrons = get_patrons(communities)
    return patrons

@router.post('/community', status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_user_access_token)])
async def create_community(community: CreateCommunityModel, user: dict = Depends(verify_user_access_token)):
    pass