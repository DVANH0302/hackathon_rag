"""thay document embedding table

Revision ID: 0845b103e03a
Revises: b2b8264326ed
Create Date: 2024-09-05 12:59:17.718094

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0845b103e03a'
down_revision: Union[str, None] = 'b2b8264326ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
