"""Add location data

Revision ID: a7f28e6440d6
Revises: db67d4159037
Create Date: 2025-04-09 21:54:19.855639

"""

from typing import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a7f28e6440d6"
down_revision: str | None = "db67d4159037"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    print("-> Populating locations")
    with open("migrations/locations.sql") as file:
        for stmt in [stmt.strip() for stmt in file.read().split(";") if stmt.strip()]:
            op.execute(sa.text(stmt))
    print("   Finished populating locations")


def downgrade() -> None:
    op.execute("TRUNCATE TABLE supermarket_price CASCADE")
