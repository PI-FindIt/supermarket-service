from typing import Optional

import strawberry
from strawberry.federation.schema_directives import Key, Shareable
from strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyMapper

from src import models
from src.crud.location import crud_location
from src.crud.prices import crud_price
from src.crud.supermarket import crud_supermarket
from src.filters import SupermarketLocationFilter, SupermarketFilter

strawberry_sqlalchemy_mapper = StrawberrySQLAlchemyMapper()


@strawberry.federation.type(keys=["ean"], extend=True)
class Product:
    ean: str

    @strawberry.field()
    async def supermarkets(self) -> list["SupermarketWithPrice"]:
        async with crud_price.get_session() as session:
            objects = await crud_price.get_by_product(self.ean, session)
            return [
                SupermarketWithPrice(
                    id=obj.supermarket_id,
                    ean=obj.product_ean,
                    price=obj.price,
                    supermarket=supermarket,
                )
                for obj in objects
                if (supermarket := await obj.awaitable_attrs.supermarket)
            ]


@strawberry_sqlalchemy_mapper.type(models.SupermarketLocation, use_federation=True)
class SupermarketLocation:
    __exclude__ = ["supermarket"]

    @strawberry.field()
    async def supermarket(self) -> Optional["Supermarket"]:
        obj = await crud_supermarket.get(self.supermarket_id)
        return Supermarket(**obj.to_dict()) if obj else None


@strawberry_sqlalchemy_mapper.type(
    models.Supermarket, use_federation=True, directives=[Key(fields="id"), Shareable()]
)
class Supermarket:
    __exclude__ = ["locations", "prices"]

    @strawberry.field()
    async def locations(self) -> list[SupermarketLocation]:
        objects = await crud_location.get_by_supermarket(self.id)  # type: ignore
        return [SupermarketLocation(**obj.to_dict()) for obj in objects]

    @strawberry.field()
    async def products(self) -> list["ProductWithPrice"]:
        objects = await crud_price.get_by_supermarket(self.id)  # type: ignore
        return [
            ProductWithPrice(price=obj.price, product=Product(ean=obj.product_ean))
            for obj in objects
        ]

    @classmethod
    async def resolve_reference(cls, id: int) -> Optional["Supermarket"]:
        model = await crud_supermarket.get(id)
        return Supermarket(**model.to_dict()) if model else None


@strawberry.federation.type(keys=["id", "ean"])
class SupermarketWithPrice:
    id: int
    ean: str
    price: float
    supermarket: Supermarket

    @classmethod
    async def resolve_reference(
        cls, id: int, ean: str
    ) -> Optional["SupermarketWithPrice"]:
        model = await crud_price.get((id, ean))
        if model is None:
            return None
        return SupermarketWithPrice(
            id=id, ean=ean, price=model.price, supermarket=model.supermarket
        )


@strawberry.type()
class ProductWithPrice:
    price: float
    product: Product


strawberry_sqlalchemy_mapper.finalize()


@strawberry.type
class Query:
    @strawberry.field()
    async def supermarket_location(
        self, supermarket_id: int, id: int
    ) -> SupermarketLocation | None:
        obj = await crud_location.get((supermarket_id, id))
        return SupermarketLocation(**obj.to_dict()) if obj else None

    @strawberry.field()
    async def supermarket_locations(
        self, filters: SupermarketLocationFilter
    ) -> list[SupermarketLocation]:
        objects = await crud_location.get_all(filters)
        return [SupermarketLocation(**obj.to_dict()) for obj in objects]

    @strawberry.field()
    async def supermarket(self, id: int) -> Supermarket | None:
        obj = await crud_supermarket.get(id)
        return Supermarket(**obj.to_dict()) if obj else None

    @strawberry.field()
    async def supermarkets(self, filters: SupermarketFilter) -> list[Supermarket]:
        objects = await crud_supermarket.get_all(filters)
        return [Supermarket(**obj.to_dict()) for obj in objects]
