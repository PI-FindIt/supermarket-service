"""Populate prices

Revision ID: db67d4159037
Revises: 18b6d3ec7226
Create Date: 2025-04-09 01:05:21.410432

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "db67d4159037"
down_revision: str | None = "18b6d3ec7226"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    print("-> Populating prices")
    with open("migrations/prices.sql") as file:
        for stmt in [stmt.strip() for stmt in file.read().split(";") if stmt.strip()]:
            op.execute(sa.text(stmt))
    print("   Finished populating prices")


def downgrade() -> None:
    op.execute("TRUNCATE TABLE supermarket_price CASCADE")
