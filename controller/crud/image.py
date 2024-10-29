from models.image import Image
from controller.crud.crud import CRUD
from sqlalchemy import select
from controller.errors.http.exceptions import not_found


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
