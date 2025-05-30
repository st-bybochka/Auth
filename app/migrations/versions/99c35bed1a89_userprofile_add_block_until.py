"""USerProfile: add block_until

Revision ID: 99c35bed1a89
Revises: de8b9af36d53
Create Date: 2025-04-17 07:00:15.363688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99c35bed1a89'
down_revision: Union[str, None] = 'de8b9af36d53'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profile', sa.Column('login_attempts', sa.Integer(), nullable=False))
    op.add_column('user_profile', sa.Column('block_until', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_profile', 'block_until')
    op.drop_column('user_profile', 'login_attempts')
    # ### end Alembic commands ###
