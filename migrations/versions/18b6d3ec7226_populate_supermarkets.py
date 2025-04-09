"""Populate supermarkets

Revision ID: 18b6d3ec7226
Revises: 8dc3b8b3ecff
Create Date: 2025-04-08 23:58:12.498805

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

revision: str = "18b6d3ec7226"
down_revision: Union[str, None] = "8dc3b8b3ecff"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with open("migrations/supermarket.sql") as file:
        for stmt in [stmt.strip() for stmt in file.read().split(";") if stmt.strip()]:
            op.execute(sa.text(stmt))


def downgrade() -> None:
    op.execute("TRUNCATE TABLE supermarket CASCADE")
