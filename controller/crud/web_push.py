from database.session import session as db_session
from sqlalchemy import select
from models.web_push import WebPush
from controller.errors.http.exceptions import internal_server_error

SESSION = db_session


class WebPushCrud:
    def __init__(self) -> None:
        self.session = SESSION

    async def create_web_push(self, web_push: WebPush) -> WebPush:
        async with self.session() as session:
            try:
                session.add(web_push)
                await session.commit()
                return web_push
            except Exception as error:
                await session.rollback()
                raise internal_server_error(str(error))