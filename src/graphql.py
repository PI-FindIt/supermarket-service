from typing import Optional

import strawberry
from strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyMapper

from src import models
from src.crud.base import Operator
from src.crud.location import crud_location
from src.crud.prices import crud_price
from src.crud.supermarket import crud_supermarket

strawberry_sqlalchemy_mapper = StrawberrySQLAlchemyMapper()


@strawberry.federation.type(keys=["ean"], extend=True)
class Product:
    ean: str

    @strawberry.field()
    async def supermarkets(self) -> list["SupermarketWithPrice"]:
        objects = await crud_price.get_by_product(self.ean)
        return [
            SupermarketWithPrice(price=obj.price, supermarket=obj.supermarket)
            for obj in objects
        ]


@strawberry_sqlalchemy_mapper.type(models.SupermarketLocation, use_federation=True)
class SupermarketLocation: ...


@strawberry_sqlalchemy_mapper.type(models.Supermarket, use_federation=True)
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


@strawberry.input()
class Filter[T]:
    value: T
    op: Operator


@strawberry.input()
class SupermarketFilter:
    ean: Optional[Filter[str]] = None
    name: Optional[Filter[str]] = None
    generic_name: Optional[Filter[str]] = None
    ingredients: Optional[Filter[str]] = None
    quantity: Optional[Filter[str]] = None
    unit: Optional[Filter[str]] = None
    keywords: Optional[Filter[list[str]]] = None
    images: Optional[Filter[list[str]]] = None
    brand_name: Optional[Filter[str]] = None
    category_name: Optional[Filter[str]] = None


@strawberry.type()
class SupermarketWithPrice:
    price: float
    supermarket: Supermarket


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
    async def supermarket(self, id: int) -> Supermarket | None:
        obj = await crud_supermarket.get(id)
        return Supermarket(**obj.to_dict()) if obj else None

    @strawberry.field()
    async def supermarkets(self, filters: SupermarketFilter) -> list[Supermarket]:
        objects = await crud_supermarket.get_all(filters)
        return [Supermarket(**obj.to_dict()) for obj in objects]
