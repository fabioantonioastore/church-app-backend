from models.image import Image
from controller.crud.crud import CRUD
from sqlalchemy import select
from controller.errors.http.exceptions import not_found, internal_server_error


class ImageCrud(CRUD):
    def __init__(self) -> None:
        super().__init__()

    async def get_image_by_id(self, image_id: str):
        async with self.session() as session:
            try:
                statement = select(Image).filter(Image.id == image_id)
                image = await session.execute(statement)
                image = image.scalars().first()
                return image
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")

    async def create_image(self, image: Image) -> Image:
        async with self.session() as session:
            try:
                session.add(image)
                await session.commit()
                return image
            except Exception as error:
                await session.rollback()
                raise error

    async def delete_image_by_id(self, image_id: str) -> str:
        async with self.session() as session:
            try:
                statement = select(Image).filter(Image.id == image_id)
                image = await session.execute(statement)
                image = image.scalars().one()
                await session.delete(image)
                await session.commit()
                return "deleted"
            except Exception as error:
                await session.rollback()
                raise not_found(f"A error occurs during CRUD: {error!r}")
