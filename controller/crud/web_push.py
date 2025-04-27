from controller.crud.crud import CRUD
from sqlalchemy import select
from models import WebPush
from controller.errors.http.exceptions import internal_server_error
from sqlalchemy.orm import selectinload
from typing import AsyncIterator
from models import User


class WebPushCrud(CRUD):
    def __init__(self) -> None:
        super().__init__()

    async def create_web_push(self, web_push: WebPush) -> WebPush:
        async with self.session() as session:
            try:
                session.add(web_push)
                await session.commit()
                return web_push
            except Exception as error:
                await session.rollback()
                raise internal_server_error(str(error))

    async def get_web_pushes_paginated(
        self, page: int = 1, page_size: int = 100
    ) -> AsyncIterator:
        async with self.session() as session:
            try:
                offset = (page - 1) * page_size
                statement = (
                    select(WebPush)
                    .options(selectinload(WebPush.user))
                    .offset(offset)
                    .limit(page_size)
                )
                web_pushes = await session.execute(statement)
                web_pushes = web_pushes.scalars().all()
                yield web_pushes
            except Exception as error:
                await session.rollback()
                raise internal_server_error(f"A error occurs during CRUD: {error!r}")

    async def get_web_push_by_user_id(self, user_id: str) -> WebPush:
        async with self.session() as session:
            try:
                statement = select(WebPush).filter(WebPush.user_id == user_id)
                web_push = await session.execute(statement)
                return web_push.scalars().first()
            except Exception as error:
                await session.rollback()
                raise error

    async def delete_web_push(self, web_push: WebPush) -> str:
        async with self.session() as session:
            try:
                await session.delete(web_push)
                await session.commit()
                return "deleted"
            except Exception as error:
                await session.rollback()
                raise error

    async def delete_web_push_by_user_id(self, user_id: str) -> str:
        async with self.session() as session:
            try:
                statement = select(WebPush).filter(WebPush.user_id == user_id)
                web_push = await session.execute(statement)
                web_push = web_push.scalars().first()
                await session.delete(web_push)
                await session.commit()
                return "deleted"
            except Exception as error:
                await session.rollback()
                raise error

    async def get_all_tokens(self) -> [WebPush]:
        async with self.session() as session:
            try:
                statement = select(WebPush)
                tokens = await session.execute(statement)
                return tokens.scalars().all()
            except Exception as error:
                await session.rollback()
                raise error
