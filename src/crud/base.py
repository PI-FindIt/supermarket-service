from contextlib import asynccontextmanager
from enum import Enum
from typing import AsyncGenerator, Callable, Any

from fastapi_cache.coder import PickleCoder
from fastapi_cache.decorator import cache
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


def _get_filter_value(filter_obj: Any) -> Any:
    """Função auxiliar para extrair valores de forma segura"""
    if filter_obj is None:
        return None

    if hasattr(filter_obj, 'value') and hasattr(filter_obj, 'op'):
        return {
            'value': _get_filter_value(filter_obj.value),
            'op': str(filter_obj.op)
        }

    if hasattr(filter_obj, '__dict__'):
        return {
            k: _get_filter_value(v)
            for k, v in vars(filter_obj).items()
            if v is not None
        }

    if isinstance(filter_obj, (list, tuple)):
        return tuple(_get_filter_value(x) for x in filter_obj)

    if isinstance(filter_obj, (str, int, float, bool)):
        return filter_obj

    return str(filter_obj)


def crud_get_key_builder(
    func: Callable[..., Any],
    namespace: str = "",
    *args: Any,
    **kwargs: Any,
) -> str:
    print(kwargs, "KW")
    self_instance = kwargs["args"][0] if kwargs else None
    model_name = self_instance.model.__name__ if self_instance else ""
    id = kwargs["args"][1] if len(kwargs["args"]) > 1 else None
    return f"{namespace}crud:{model_name}:get:{id}"

def crud_get_all_key_builder(
    func: Callable[..., Any],
    namespace: str = "",
    *args: Any,
    **kwargs: Any,
) -> str:
    self_instance = kwargs["args"][0] if kwargs else None
    model_name = self_instance.model.__name__ if self_instance else ""
    filters = kwargs["args"][1] if len(kwargs["args"]) > 1 else []

    if filters:
        filter_dict = _get_filter_value(filters)
        filter_items = sorted(
            (str(k), str(v)) for k, v in filter_dict.items()
        )
        filter_hash = hash(tuple(filter_items))
        return f"{namespace}crud:{model_name}:get_all:{filter_hash}"

    return f"{namespace}crud:{model_name}:get_all"

class CrudBase[T: Base, F, K: int | tuple[int | str, ...]]:
    """
    Base CRUD class for all models.

    Generic type model is the model class, F is the filter class, and K is the key type.
    """

    def __init__(
        self,
        model: type[T],
        filter: type[F] | None,
    ) -> None:
        self.model = model
        self.filter = filter

    @staticmethod
    @asynccontextmanager
    async def get_session(
        session: AsyncSession | None = None,
    ) -> AsyncGenerator[AsyncSession, None]:
        if session is not None:
            yield session
            return
        async with get_postgres_session() as session:
            yield session

    @cache(
        expire=60,
        key_builder=crud_get_key_builder,
        coder=PickleCoder,
    )
    async def get(self, id: K, session: AsyncSession | None = None) -> T | None:
        async with self.get_session(session) as session:
            return await session.get(self.model, id)

    @cache(
        expire=60,
        key_builder=crud_get_all_key_builder,
        coder=PickleCoder,
    )
    async def get_all(
        self,
        filters: F,
        session: AsyncSession | None = None,
    ) -> list[T]:
        async with self.get_session(session) as session:
            query = select(self.model)
            if self.filter is not None:
                for key, value in [
                    (column.key, getattr(filters, column.key))
                    for column in self.model.__table__.columns
                    if column.key != "logo" and getattr(filters, column.key) is not None
                ]:
                    query = operations(self.model)[value.op](query, key, value.value)
            result = await session.execute(query)
            return result.scalars().all()
