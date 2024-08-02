from models.community import Community
from uuid import uuid4

def get_patrons(communities: [Community]) -> list:
    return [community.patron for community in communities]

def create_community_data(community_data: dict) -> Community:
    community = Community()
    for key in community_data:
        match key:
            case "patron":
                community.patron = community_data['patron']
            case "image":
                community.image = community_data['image']
            case "location":
                community.location = community_data['location']
            case "email":
                community.email = community_data['email']
    community.id = str(uuid4())
    return community

def convert_to_dict(community: Community) -> dict:
    new_community = {'id': community.id, 'patron': community.patron, 'email': community.email, 'image': community.image,
                     'location': community.location}
    return new_community

def get_community_client_data(community: Community) -> dict:
    community_data = {'patron': community.patron, 'location': community.location, 'email': community.email,
                      'image': community.image}
    return community_data