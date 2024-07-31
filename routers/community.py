from fastapi import APIRouter, status
from controller.crud.community import CommunityCrud
from database.session import session
from controller.src.community import get_patrons

router = APIRouter()
community_crud = CommunityCrud()

@router.get('/patrons', status_code=status.HTTP_200_OK)
async def get_all_patrons():
    communities = await community_crud.get_all_communities(session)
    patrons = get_patrons(communities)
    return patrons