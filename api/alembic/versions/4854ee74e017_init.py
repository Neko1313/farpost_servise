"""init

Revision ID: 4854ee74e017
Revises: 
Create Date: 2024-01-06 15:40:45.864739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4854ee74e017'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_farpost',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('abs',
    sa.Column('abs_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('link_main_img', sa.String(), nullable=False),
    sa.Column('link', sa.String(), nullable=False),
    sa.Column('name_farpost', sa.String(), nullable=False),
    sa.Column('city_english', sa.String(), nullable=False),
    sa.Column('categore', sa.String(), nullable=False),
    sa.Column('subcategories', sa.String(), nullable=False),
    sa.Column('category_attribute', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user_farpost.user_id'], ),
    sa.PrimaryKeyConstraint('abs_id')
    )
    op.create_table('abs_active',
    sa.Column('abs_active_id', sa.Uuid(), nullable=False),
    sa.Column('abs_id', sa.Integer(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('price_limitation', sa.Float(), nullable=False),
    sa.Column('date_creation', sa.TIMESTAMP(), nullable=False),
    sa.Column('date_closing', sa.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['abs_id'], ['abs.abs_id'], ),
    sa.PrimaryKeyConstraint('abs_active_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('abs_active')
    op.drop_table('abs')
    op.drop_table('user_farpost')
    # ### end Alembic commands ###
