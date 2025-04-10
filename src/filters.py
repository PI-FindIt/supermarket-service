from typing import Optional

import strawberry

from src.crud.base import Operator
from src.models import SupermarketServices


@strawberry.input()
class Filter[T]:
    value: T
    op: Operator


@strawberry.input()
class SupermarketFilter:
    id: Optional[Filter[int]] = None
    name: Optional[Filter[str]] = None
    image: Optional[Filter[str]] = None
    services: Optional[Filter[list[SupermarketServices]]] = None
    description: Optional[Filter[str]] = None


@strawberry.input()
class Coordinate:
    latitude: float
    longitude: float
    distance: float


@strawberry.input()
class SupermarketLocationFilter:
    supermarket_id: Optional[Filter[int]] = None
    id: Optional[Filter[int]] = None
    name: Optional[Filter[str]] = None
    image: Optional[Filter[str]] = None
    coordinates: Optional[Filter[Coordinate]] = (
        None  # (latitude, longitude, distance in km)
    )
