from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import CrudBase
from src.models import SupermarketLocation


class CrudLocation(CrudBase[SupermarketLocation, None, tuple[int, int]]):
    def __init__(self) -> None:
        super().__init__(SupermarketLocation, None)

    async def get_by_supermarket(
        self, id: int, session: AsyncSession | None = None
    ) -> list[SupermarketLocation]:
        async with self.get_session(session) as session:
            query = select(SupermarketLocation).where(
                SupermarketLocation.supermarket_id == id
            )
            result = await session.execute(query)
            return result.scalars().all()


crud_location = CrudLocation()
