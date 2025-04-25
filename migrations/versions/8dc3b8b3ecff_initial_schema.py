"""Initial schema

Revision ID: 8dc3b8b3ecff
Revises:
Create Date: 2025-04-08 19:40:03.603070

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8dc3b8b3ecff"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "supermarket",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("logo", sa.String(), nullable=True),
        sa.Column("logo_blurhash", sa.String(), nullable=True),
        sa.Column("image", sa.String(), nullable=True),
        sa.Column("image_blurhash", sa.String(), nullable=True),
        sa.Column(
            "services",
            sa.ARRAY(
                sa.Enum(
                    "COFFEE",
                    "GAS_STATION",
                    "NEWSSTAND",
                    "PHARMACY",
                    "RESTAURANT",
                    "SELF_KIOSK",
                    name="supermarketservices",
                )
            ),
            nullable=False,
        ),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_supermarket_services"), "supermarket", ["services"], unique=False
    )

    op.create_table(
        "supermarket_location",
        sa.Column("supermarket_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["supermarket_id"],
            ["supermarket.id"],
        ),
        sa.PrimaryKeyConstraint("supermarket_id", "id"),
    )
    op.create_index(
        op.f("ix_supermarket_location_supermarket_id"),
        "supermarket_location",
        ["supermarket_id"],
        unique=False,
    )

    op.create_table(
        "supermarket_price",
        sa.Column("supermarket_id", sa.Integer(), nullable=False),
        sa.Column("product_ean", sa.String(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["supermarket_id"],
            ["supermarket.id"],
        ),
        sa.PrimaryKeyConstraint("supermarket_id", "product_ean"),
    )
    op.create_index(
        op.f("ix_supermarket_price_product_ean"),
        "supermarket_price",
        ["product_ean"],
        unique=False,
    )
    op.create_index(
        op.f("ix_supermarket_price_supermarket_id"),
        "supermarket_price",
        ["supermarket_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_supermarket_price_supermarket_id"), table_name="supermarket_price"
    )
    op.drop_index(
        op.f("ix_supermarket_price_product_ean"), table_name="supermarket_price"
    )
    op.drop_table("supermarket_price")
    op.drop_index(
        op.f("ix_supermarket_location_supermarket_id"),
        table_name="supermarket_location",
    )
    op.drop_table("supermarket_location")
    op.drop_index(op.f("ix_supermarket_services"), table_name="supermarket")
    op.drop_table("supermarket")
