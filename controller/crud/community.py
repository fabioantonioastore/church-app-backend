from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from models.community import Community
from controller.errors.http.exceptions import not_found

class CommunityCrud:
    async def get_all_communities(self, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            try:
                statement = select(Community)
                communities = await session.execute(statement)
                return communities.scalars().all()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")
    async def get_community_by_patron(self, async_session: async_sessionmaker[AsyncSession], community_patron: str):
        async with async_session() as session:
            try:
                statement = select(Community).filter(Community.patron == community_patron)
                community = await session.execute(statement)
                return community.scalars().one()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_community_by_id(self, async_session: async_sessionmaker[AsyncSession], community_id: str):
        async with async_session() as session:
            try:
                statement = select(Community).filter(Community.id == community_id)
                community = await session.execute(statement)
                return community.scalars().one()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def create_community(self, async_session: async_sessionmaker[AsyncSession], community: Community):
        async with async_session() as session:
            try:
                session.add(community)
                await session.commit()
                return community
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

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
                        case 'active':
                            community.active = new_community['active']
                await session.commit()
                return community
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def delete_community(self, async_session: async_sessionmaker[AsyncSession], community: Community):
        async with async_session() as session:
            try:
                await session.delete(community)
                await session.commit()
                return f"{community} deleted with successfull"
            except:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def delete_community_by_id(self, async_session: async_sessionmaker[AsyncSession], community_id: str):
        async with async_session() as session:
            try:
                statement = select(Community).filter(Community.id == community_id)
                community = await session.execute(statement)
                community = community.scalars().one()
                await session.delete(community)
                await session.commit()
                return f"{community} deleted with succesfull"
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")