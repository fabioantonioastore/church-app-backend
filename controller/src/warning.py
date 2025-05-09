from models import Warning
from uuid import uuid4
from datetime import datetime
from controller.src.warning_view import get_warning_view_no_sensitive_data


async def create_warning(warning: dict) -> Warning:
    new_warning = Warning()
    for key in warning:
        match key:
            case "title":
                new_warning.title = warning["title"]
            case "description":
                new_warning.description = warning["description"]
            case "image":
                new_warning.image = warning["image"]
            case "scope":
                new_warning.scope = warning["scope"]
            case "community_id":
                new_warning.community_id = warning["community_id"]
            case "posted_by":
                new_warning.posted_by = warning["posted_by"]
    new_warning.id = str(uuid4())
    new_warning.posted_at = datetime.now()
    return new_warning


async def get_warning_client_data(warning: Warning, client: bool = True) -> dict:
    new_warning = {
        "id": warning.id,
        "title": warning.title,
        "description": warning.description,
        "posted_at": warning.posted_at,
        "image": warning.image,
        "scope": warning.scope,
        "edited_at": warning.edited_at,
        "posted_by": warning.posted_by,
        "views": await get_warning_view_no_sensitive_data(warning.id, client),
    }
    return new_warning
