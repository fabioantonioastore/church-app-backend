from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from models.board_member import BoardMember
from sqlalchemy import select
from controller.errors.database_error import DatabaseError

class BoardMemberCrud:
    async def get_board_member_by_id(self, async_session: async_sessionmaker[AsyncSession], board_member_id: str):
        async with async_session() as session:
            try:
                statement = select(BoardMember).filter(BoardMember.id == board_member_id)
                board_member = await session.execute(statement)
                return board_member.scalars().one()
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def get_board_member_by_cpf(self, async_session: async_sessionmaker[AsyncSession], board_member_cpf: str):
        async with async_session() as session:
            try:
                statement = select(BoardMember).filter(BoardMember.cpf == board_member_cpf)
                board_member = await session.execute(statement)
                return board_member.scalars().one()
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def create_board_member(self, async_session: async_sessionmaker[AsyncSession], board_member: BoardMember):
        async with async_session() as session:
            try:
                session.add(board_member)
                await session.commit()
                return board_member
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def update_board_member(self, async_session: async_sessionmaker[AsyncSession], new_board_member: dict):
        async with async_session() as session:
            try:
                statement = select(BoardMember).filter(BoardMember.id == new_board_member['id'])
                board_member = await session.execute(statement)
                board_member = board_member.scalars().one()
                for key in new_board_member.keys():
                    match key:
                        case 'position':
                            board_member.position = new_board_member['position']
                await session.commit()
                return board_member
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def delete_board_member(self, async_session: async_sessionmaker[AsyncSession], board_member: BoardMember):
        async with async_session() as session:
            try:
                await session.delete(board_member)
                await session.commit()
                return f"{board_member} deleted with succesfull"
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def delete_board_member_by_id(self, async_session: async_sessionmaker[AsyncSession], board_member_id):
        async with async_session() as session:
            try:
                statement = select(BoardMember).filter(BoardMember.id == board_member_id)
                board_member = await session.execute(statement)
                board_member = board_member.scalars().one()
                await session.delete(board_member)
                await session.commit()
                return f"{board_member} deleted with succesfull"
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error

    async def delete_board_member_by_cpf(self, async_session: async_sessionmaker[AsyncSession], board_member_cpf: str):
        async with async_session() as session:
            try:
                statement = select(BoardMember).filter(BoardMember.cpf == board_member_cpf)
                board_member = await session.execute(statement)
                board_member = board_member.scalars().one()
                await session.delete(board_member)
                await session.commit()
                return f"{board_member} deleted with succesfull"
            except DatabaseError as database_error:
                await session.rollback()
                raise database_error