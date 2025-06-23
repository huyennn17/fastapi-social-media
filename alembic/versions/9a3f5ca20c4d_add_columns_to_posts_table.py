"""add columns to posts table

Revision ID: 9a3f5ca20c4d
Revises: 248aca947d8d
Create Date: 2025-06-23 09:32:51.959978

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a3f5ca20c4d'
down_revision: Union[str, Sequence[str], None] = '248aca947d8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
