"""add workflow_mode

Revision ID: 5bb761a2689d
Revises: af4a4574efbf
Create Date: 2026-08-09 01:19:05.245341
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "5bb761a2689d"
down_revision: Union[str, Sequence[str], None] = "af4a4574efbf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


workflow_mode_enum = sa.Enum(
    "NEW_ORDER",
    "MODIFY_ORDER",
    name="workflowmode",
)


def upgrade() -> None:
    """Upgrade schema."""

    bind = op.get_bind()

    # Create PostgreSQL enum type
    workflow_mode_enum.create(
        bind,
        checkfirst=True,
    )

    # Add column
    op.add_column(
        "order_drafts",
        sa.Column(
            "workflow_mode",
            workflow_mode_enum,
            nullable=False,
            server_default="NEW_ORDER",
        ),
    )

    # Remove temporary default
    op.alter_column(
        "order_drafts",
        "workflow_mode",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    bind = op.get_bind()

    op.drop_column(
        "order_drafts",
        "workflow_mode",
    )

    workflow_mode_enum.drop(
        bind,
        checkfirst=True,
    )