"""Populate supermarkets

Revision ID: 18b6d3ec7226
Revises: 8dc3b8b3ecff
Create Date: 2025-04-08 23:58:12.498805

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "18b6d3ec7226"
down_revision: str | None = "8dc3b8b3ecff"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    print("-> Populating supermarkets")
    with open("migrations/supermarket.sql") as file:
        for stmt in [stmt.strip() for stmt in file.read().split(";\n") if stmt.strip()]:
            op.execute(sa.text(stmt))
    print("   Finished populating supermarkets")


def downgrade() -> None:
    op.execute("TRUNCATE TABLE supermarket_location CASCADE")
