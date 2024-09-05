"""thay documents table

Revision ID: 001c54750848
Revises: 4c14f3aa4eed
Create Date: 2024-09-04 23:06:30.054098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001c54750848'
down_revision: Union[str, None] = '4c14f3aa4eed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
