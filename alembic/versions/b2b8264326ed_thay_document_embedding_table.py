"""thay document embedding table

Revision ID: b2b8264326ed
Revises: 001c54750848
Create Date: 2024-09-05 12:03:16.960926

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2b8264326ed'
down_revision: Union[str, None] = '001c54750848'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
