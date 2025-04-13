from enum import Enum
from typing import Any

from sqlalchemy import ARRAY, ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    def to_dict(self) -> dict[str, Any]:
        return {field.name: getattr(self, field.name) for field in self.__table__.c}


class SupermarketServices(Enum):
    COFFEE = "coffee"
    GAS_STATION = "gas_station"
    NEWSSTAND = "newsstand"
    PHARMACY = "pharmacy"
    RESTAURANT = "restaurant"
    SELF_KIOSK = "self_kiosk"


class Supermarket(Base):
    __tablename__ = "supermarket"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    logo: Mapped[str | None] = mapped_column(default=None)
    image: Mapped[str | None] = mapped_column(default=None)
    services: Mapped[list[SupermarketServices]] = mapped_column(
        ARRAY(SQLAlchemyEnum(SupermarketServices)), index=True
    )
    description: Mapped[str | None] = mapped_column(default=None)
    locations: Mapped[list["SupermarketLocation"]] = relationship(
        back_populates="supermarket"
    )
    prices: Mapped[list["SupermarketPrice"]] = relationship(
        back_populates="supermarket", cascade="all, delete-orphan"
    )


class SupermarketLocation(Base):
    __tablename__ = "supermarket_location"
    supermarket_id: Mapped[int] = mapped_column(
        ForeignKey("supermarket.id"), index=True, primary_key=True
    )
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str | None] = mapped_column(default=None, nullable=True)
    latitude: Mapped[float]
    longitude: Mapped[float]
    supermarket: Mapped[Supermarket] = relationship(back_populates="locations")


class SupermarketPrice(Base):
    __tablename__ = "supermarket_price"
    supermarket_id: Mapped[int] = mapped_column(
        ForeignKey("supermarket.id"), index=True, primary_key=True
    )
    product_ean: Mapped[str] = mapped_column(index=True, primary_key=True)
    price: Mapped[float]
    supermarket: Mapped[Supermarket] = relationship(back_populates="prices")
