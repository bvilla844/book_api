"""add revie_text to review table

Revision ID: d44be04b7b4b
Revises: 9f67c538b06b
Create Date: 2025-05-16 10:40:21.968435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'd44be04b7b4b'
down_revision: Union[str, None] = '9f67c538b06b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviews', sa.Column('review_text', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reviews', 'review_text')
    # ### end Alembic commands ###
