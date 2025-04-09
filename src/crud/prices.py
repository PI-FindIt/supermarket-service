from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import CrudBase
from src.models import SupermarketPrice


class CrudPrice(CrudBase[SupermarketPrice, None, tuple[int, str]]):
    def __init__(self) -> None:
        super().__init__(SupermarketPrice, None)

    async def get_by_supermarket(
        self, id: int, session: AsyncSession | None = None
    ) -> list[SupermarketPrice]:
        async with self.get_session(session) as session:
            query = select(SupermarketPrice).where(
                SupermarketPrice.supermarket_id == id
            )
            result = await session.execute(query)
            return result.scalars().all()

    async def get_by_product(
        self, ean: str, session: AsyncSession | None = None
    ) -> list[SupermarketPrice]:
        async with self.get_session(session) as session:
            query = select(SupermarketPrice).where(SupermarketPrice.product_ean == ean)
            result = await session.execute(query)
            return result.scalars().all()


crud_price = CrudPrice()
