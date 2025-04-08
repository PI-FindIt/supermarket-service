from contextlib import asynccontextmanager
from enum import Enum
from typing import AsyncGenerator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.session import get_postgres_session
from src.models import Base


class Operator(Enum):
    EQ = "=="
    NE = "!="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    LIKE = "like"
    ILIKE = "ilike"
    IN = "in"
    NOT_IN = "not in"
    IS = "is"
    IS_NOT = "is not"
    CONTAINS = "contains"
    NOT_CONTAINS = "not contains"
    ANY = "any"
    ALL = "all"


operations = lambda model: {
    Operator.EQ: lambda q, k, v: q.where(getattr(model, k) == v),
    Operator.NE: lambda q, k, v: q.where(getattr(model, k) != v),
    Operator.LT: lambda q, k, v: q.where(getattr(model, k) < v),
    Operator.LE: lambda q, k, v: q.where(getattr(model, k) <= v),
    Operator.GT: lambda q, k, v: q.where(getattr(model, k) > v),
    Operator.GE: lambda q, k, v: q.where(getattr(model, k) >= v),
    Operator.LIKE: lambda q, k, v: q.where(getattr(model, k).like(v)),
    Operator.ILIKE: lambda q, k, v: q.where(getattr(model, k).ilike(v)),
    Operator.IN: lambda q, k, v: q.where(getattr(model, k).in_(v)),
    Operator.NOT_IN: lambda q, k, v: q.where(getattr(model, k).notin_(v)),
    Operator.IS: lambda q, k, v: q.where(getattr(model, k).is_(v)),
    Operator.IS_NOT: lambda q, k, v: q.where(getattr(model, k).isnot(v)),
    Operator.CONTAINS: lambda q, k, v: q.where(getattr(model, k).contains(v)),
    Operator.NOT_CONTAINS: lambda q, k, v: q.where(getattr(model, k).notcontains(v)),
    Operator.ANY: lambda q, k, v: q.where(getattr(model, k).any(v)),
    Operator.ALL: lambda q, k, v: q.where(getattr(model, k).all(v)),
}


class CrudBase[T: Base, F, K: int | tuple[int | str, ...]]:
    """
    Base CRUD class for all models.

    Generic type model is the model class, F is the filter class, and K is the key type.
    """

    def __init__(self, model: type[T], filter: type[F] | None) -> None:
        self.model = model
        self.filter = filter

    @staticmethod
    @asynccontextmanager
    async def _get_session(
        session: AsyncSession | None = None,
    ) -> AsyncGenerator[AsyncSession, None]:
        if session is not None:
            yield session
            return
        async with get_postgres_session() as session:
            yield session

    async def get(self, id: K, session: AsyncSession | None = None) -> T | None:
        async with self._get_session(session) as session:
            return await session.get(self.model, id)

    async def get_all(
        self,
        filters: F,
        session: AsyncSession | None = None,
    ) -> list[T]:
        async with self._get_session(session) as session:
            query = select(self.model)  # type: ignore
            if self.filter is not None:
                for key, value in [
                    (column.key, getattr(filters, column.key))
                    for column in self.model.__table__.columns
                    if getattr(filters, column.key) is not None
                ]:
                    query = operations(self.model)[value.op](query, key, value.value)
            result = await session.execute(query)
            return result.scalars().all()
