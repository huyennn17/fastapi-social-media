"""add content column to posts table

Revision ID: 9c4c6292d39f
Revises: 84bbcb357ccc
Create Date: 2025-06-23 09:15:55.442713

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c4c6292d39f'
down_revision: Union[str, Sequence[str], None] = '84bbcb357ccc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(length=255), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
