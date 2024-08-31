from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from typing import AsyncIterator
from models.community import Community
from controller.errors.http.exceptions import not_found, internal_server_error

class CommunityCrud:
    async def get_communities_paginated(self, async_session: async_sessionmaker[AsyncSession], page: int = 1, page_size: int = 100) -> AsyncIterator:
        async with async_session() as session:
            try:
                offset = (page - 1) * page_size
                statement = select(Community).offset(offset).limit(page_size)
                communities = await session.execute(statement)
                communities = communities.scalars().all()
                yield communities
            except Exception as error:
                await session.rollback()
                raise internal_server_error(f"A error occurs during CRUD: {error!r}")

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
            except Exception as error:
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

    async def increase_actual_month_payment_value(self, async_session: async_sessionmaker[AsyncSession], community_id: str, value: int) -> Community:
        async with async_session() as session:
            try:
                statement = select(Community).filter(Community.id == community_id)
                community = await session.execute(statement)
                community = community.scalars().one()
                community.actual_month_total_payment_value += value
                await session.commit()
                return community
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def transfer_actual_to_last_month_and_reset_actual(self, async_session: async_sessionmaker[AsyncSession], community_id: str) -> Community:
        async with async_session() as session:
            try:
                statement = select(Community).filter(Community.id == community_id)
                community = await session.execute(statement)
                community = community.scalars().one()
                community.last_month_total_payment_value = community.actual_month_total_payment_value
                community.actual_month_total_payment_value = 0
                await session.commit()
                return community
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")