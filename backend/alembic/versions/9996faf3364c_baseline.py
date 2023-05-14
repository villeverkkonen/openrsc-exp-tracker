"""baseline

Revision ID: 9996faf3364c
Revises: 
Create Date: 2023-05-14 13:39:59.938421

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9996faf3364c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'players',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(), unique=True,
                  index=True, nullable=False),
        sa.Column('original_exp', sa.Integer()),
        sa.Column('created_at', sa.DateTime()))

    op.create_table(
        'hiscores',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('new_exp', sa.Integer()),
        sa.Column('total_gained_exp', sa.Integer()),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('player_id', sa.Integer, nullable=False))


def downgrade() -> None:
    op.drop_table('hiscores')
    op.drop_table('players')
