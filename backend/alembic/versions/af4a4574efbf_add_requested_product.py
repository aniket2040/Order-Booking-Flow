"""add requested_product

Revision ID: af4a4574efbf
Revises:
Create Date: 2026-08-08 03:46:12.014347
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "af4a4574efbf"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "order_drafts",
        sa.Column(
            "requested_product",
            sa.String(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "order_drafts",
        "requested_product",
    )