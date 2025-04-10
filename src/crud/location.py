from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import CrudBase, Operator, operations
from src.filters import SupermarketLocationFilter
from src.models import SupermarketLocation


class CrudLocation(
    CrudBase[SupermarketLocation, SupermarketLocationFilter, tuple[int, int]]
):
    def __init__(self) -> None:
        super().__init__(SupermarketLocation, SupermarketLocationFilter)

    async def get_by_supermarket(
        self, id: int, session: AsyncSession | None = None
    ) -> list[SupermarketLocation]:
        async with self.get_session(session) as session:
            query = select(SupermarketLocation).where(
                SupermarketLocation.supermarket_id == id
            )
            result = await session.execute(query)
            return result.scalars().all()

    async def get_all(
        self,
        filters: SupermarketLocationFilter,
        session: AsyncSession | None = None,
    ) -> list[SupermarketLocation]:
        async with self.get_session(session) as session:
            query = select(SupermarketLocation)
            if self.filter is not None:
                for key, value in [
                    (column.key, value)
                    for column in SupermarketLocation.__table__.columns
                    if column.key not in ["latitude", "longitude"]
                    and (value := getattr(filters, column.key)) is not None
                ]:
                    query = operations(SupermarketLocation)[value.op](
                        query, key, value.value
                    )

                if filters.coordinates is not None:
                    op2 = {
                        **operations(SupermarketLocation),
                        Operator.EQ: lambda q, k, v: q.where(k == v),
                        Operator.NE: lambda q, k, v: q.where(k != v),
                        Operator.LT: lambda q, k, v: q.where(k < v),
                        Operator.LE: lambda q, k, v: q.where(k <= v),
                        Operator.GT: lambda q, k, v: q.where(k > v),
                        Operator.GE: lambda q, k, v: q.where(k >= v),
                    }
                    lat_rad = func.radians(filters.coordinates.value.latitude)
                    lon_rad = func.radians(filters.coordinates.value.longitude)
                    model_lat_rad = func.radians(SupermarketLocation.latitude)
                    model_lon_rad = func.radians(SupermarketLocation.longitude)

                    delta_lat = model_lat_rad - lat_rad
                    delta_lon = model_lon_rad - lon_rad

                    a = func.pow(func.sin(delta_lat / 2), 2) + func.cos(
                        lat_rad
                    ) * func.cos(model_lat_rad) * func.pow(func.sin(delta_lon / 2), 2)
                    distance = 6371 * 2 * func.atan2(func.sqrt(a), func.sqrt(1 - a))
                    query = op2[filters.coordinates.op](
                        query, distance, filters.coordinates.value.distance
                    )

            result = await session.execute(query)
            return result.scalars().all()


crud_location = CrudLocation()
