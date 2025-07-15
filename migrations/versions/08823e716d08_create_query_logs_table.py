"""Create query_logs table

Revision ID: 08823e716d08
Revises: 
Create Date: 2025-07-15 04:20:07.619112

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08823e716d08'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "query_logs",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("sql", sa.String, nullable=False),
        sa.Column(
            "executed_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("query_logs")
