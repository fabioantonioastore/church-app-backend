from models import Community
from uuid import uuid4
from models import User


def create_subccount(pix_key: str, name: str) -> dict:
    return {
        "pixKey": pix_key,
        "name": str
    }


def get_users_friendly_data(users: [User]) -> list[dict]:
    return [
        {
            "name": user.name,
            "birthday": user.birthday,
            "email": user.email,
            "cpf": user.cpf,
        }
        for user in users
    ]


def get_patrons(communities: [Community]) -> list:
    return [community.patron for community in communities]


def get_community_list(communities: [Community]) -> list:
    return [
        {"patron": community.patron, "location": community.location}
        for community in communities
    ]


def create_community_data(community_data: dict) -> Community:
    community = Community()
    for key in community_data:
        match key:
            case "patron":
                community.patron = community_data["patron"]
            case "image":
                community.image = community_data["image"]
            case "location":
                community.location = community_data["location"]
            case "email":
                community.email = community_data["email"]
            case "pix_key":
                community.pix_key = community_data["pix_key"]
    community.id = str(uuid4())
    return community


def convert_to_dict(community: Community) -> dict:
    new_community = {
        "id": community.id,
        "patron": community.patron,
        "email": community.email,
        "image": community.image,
        "location": community.location,
        "active": community.active,
    }
    return new_community


def get_community_client_data(community: Community) -> dict:
    community_data = {
        "patron": community.patron,
        "location": community.location,
        "email": community.email,
        "image": community.image,
        "active": community.active,
    }
    return community_data


def update_community_data(community: Community, data: dict) -> dict:
    for key in data:
        match key:
            case "patron":
                community.patron = data["patron"]
            case "email":
                community.email = data["email"]
            case "location":
                community.location = data["location"]
            case "image":
                community.image = data["image"]
    return convert_to_dict(community)


def get_community_patron(community: Community) -> str:
    return community.patron
