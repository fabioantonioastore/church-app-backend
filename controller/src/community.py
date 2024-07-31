from models.community import Community

def get_patrons(communities: [Community]) -> list:
    return [community.patron for community in communities]