from sqlalchemy import select
from typing import AsyncIterator
from models.community import Community
from controller.errors.http.exceptions import not_found, internal_server_error
from database.session import session as db_session

SESSION = db_session


class CommunityCrud:
    def __init__(self) -> None:
        self.session = SESSION

    async def get_communities_paginated(self, page: int = 1, page_size: int = 100) -> AsyncIterator:
        async with self.session() as session:
            try:
                offset = (page - 1) * page_size
                statement = select(Community).offset(offset).limit(page_size)
                communities = await session.execute(statement)
                communities = communities.scalars().all()
                yield communities
            except Exception as error:
                await session.rollback()
                raise internal_server_error(f"A error occurs during CRUD: {error!r}")

    async def get_all_communities(self):
        async with self.session() as session:
            try:
                statement = select(Community)
                communities = await session.execute(statement)
                return communities.scalars().all()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_community_by_patron(self, community_patron: str):
        async with self.session() as session:
            try:
                statement = select(Community).filter(Community.patron == community_patron)
                community = await session.execute(statement)
                return community.scalars().first()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def get_community_by_id(self, community_id: str):
        async with self.session() as session:
            try:
                statement = select(Community).filter(Community.id == community_id)
                community = await session.execute(statement)
                return community.scalars().first()
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def create_community(self, community: Community):
        async with self.session() as session:
            try:
                session.add(community)
                await session.commit()
                return community
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def update_community(self, new_community: dict):
        async with self.session() as session:
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

    async def delete_community(self, community: Community):
        async with self.session() as session:
            try:
                await session.delete(community)
                await session.commit()
                return f"{community} deleted with successfull"
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def delete_community_by_id(self, community_id: str):
        async with self.session() as session:
            try:
                statement = select(Community).filter(Community.id == community_id)
                community = await session.execute(statement)
                community = community.scalars().first()
                await session.delete(community)
                await session.commit()
                return f"{community} deleted with succesfull"
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def increase_actual_month_payment_value(self,
                                                  community_id: str, value: int) -> Community:
        async with self.session() as session:
            try:
                statement = select(Community).filter(Community.id == community_id)
                community = await session.execute(statement)
                community = community.scalars().first()
                community.actual_month_total_payment_value += value
                await session.commit()
                return community
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def transfer_actual_to_last_month_and_reset_actual(self,
                                                             community_id: str) -> Community:
        async with self.session() as session:
            try:
                statement = select(Community).filter(Community.id == community_id)
                community = await session.execute(statement)
                community = community.scalars().first()
                community.last_month_total_payment_value = community.actual_month_total_payment_value
                community.actual_month_total_payment_value = 0
                await session.commit()
                return community
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")
