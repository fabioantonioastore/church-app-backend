from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from models.community import Community
from controller.errors.http.exceptions import internal_server_error

class CommunityCrud:
    async def get_all_communities(self, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            try:
                statement = select(Community)
                communities = await session.execute(statement)
                return communities.scalars().all()
            except Exception as error:
                await session.rollback()
                raise internal_server_error("A error occurs during CRUD")
    async def get_community_by_patron(self, async_session: async_sessionmaker[AsyncSession], community_patron: str):
        async with async_session() as session:
            try:
                statement = select(Community).filter(Community.patron == community_patron)
                community = await session.execute(statement)
                return community.scalars().one()
            except:
                await session.rollback()
                raise internal_server_error("A error occurs during CRUD")
    async def get_community_by_location(self, async_session: async_sessionmaker[AsyncSession], community_location: str):
        async with async_session() as session:
            try:
                statement = select(Community).filter(Community.location == community_location)
                community = await session.execute(statement)
                return community.scalars().one()
            except:
                await session.rollback()
                raise internal_server_error("A error occurs during CRUD")
    async def get_community_by_id(self, async_session: async_sessionmaker[AsyncSession], community_id: str):
        async with async_session() as session:
            try:
                statement = select(Community).filter(Community.id == community_id)
                community = await session.execute(statement)
                return community.scalars().one()
            except:
                await session.rollback()
                raise internal_server_error("A error occurs during CRUD")

    async def create_community(self, async_session: async_sessionmaker[AsyncSession], community: Community):
        async with async_session() as session:
            try:
                session.add(community)
                await session.commit()
                return community
            except:
                await session.rollback()
                raise internal_server_error("A error occurs during CRUD")

    async def update_community(self, async_session: async_sessionmaker[AsyncSession], new_community: dict):
        async with async_session() as session:
            try:
                statement = select(Community).filter(Community.id == new_community['id'])
                community = await session.execute(statement)
                community = community.scalars().one()
                for key in new_community.keys():
                    match key:
                        case 'name':
                            community.name = new_community['name']
                        case 'patron':
                            community.patron = new_community['patron']
                        case 'email':
                            community.email = new_community['email']
                        case 'image':
                            community.image = new_community['image']
                        case 'location':
                            community.location = new_community['location']
                await session.commit()
                return community
            except:
                await session.rollback()
                raise internal_server_error("A error occurs during CRUD")

    async def delete_community(self, async_session: async_sessionmaker[AsyncSession], community: Community):
        async with async_session() as session:
            try:
                await session.delete(community)
                await session.commit()
                return f"{community} deleted with succesfull"
            except:
                await session.rollback()
                raise internal_server_error(f"A error occurs during CRUD")

    async def delete_community_by_id(self, async_session: async_sessionmaker[AsyncSession], community_id: str):
        async with async_session() as session:
            try:
                statement = select(Community).filter(Community.id == community_id)
                community = await session.execute(statement)
                community = community.scalars().one()
                await session.delete(community)
                await session.commit()
                return f"{community} deleted with succesfull"
            except:
                await session.rollback()
                raise internal_server_error("A error occurs during CRUD")