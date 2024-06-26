"""add competitor_id

Revision ID: 6bb00e6424a1
Revises: 1d95a69efe64
Create Date: 2024-02-07 01:33:00.607597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bb00e6424a1'
down_revision = '1d95a69efe64'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('abs_active', sa.Column('competitor_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('abs_active', 'competitor_id')
    # ### end Alembic commands ###
