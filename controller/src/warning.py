from models.warning import Warning
from controller.crud.community import CommunityCrud
from database.session import session
from uuid import uuid4
from datetime import datetime, timezone

community_crud = CommunityCrud()

async def create_warning(warning: dict) -> Warning:
    new_warning = Warning()
    for key in warning:
        match key:
            case "title":
                new_warning.title = warning['title']
            case "description":
                new_warning.description = warning['description']
            case "image":
                new_warning.image = warning['image']
            case "scope":
                new_warning.scope = warning['scope']
            case "community_id":
                new_warning.community_id = warning['community_id']
    new_warning.id = str(uuid4())
    new_warning.posted_at = datetime.now()
    return new_warning

def get_warning_client_data(warning: Warning) -> dict:
    new_warning = {}
    new_warning['id'] = warning.id
    new_warning['title'] = warning.title
    new_warning['description'] = warning.description
    new_warning['posted_at'] = warning.posted_at
    new_warning['image'] = warning.image
    new_warning['scope'] = warning.scope
    new_warning['edited_at'] = warning.edited_at
    return new_warning