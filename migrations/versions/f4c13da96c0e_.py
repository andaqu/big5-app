"""empty message

Revision ID: f4c13da96c0e
Revises: db7b344694d7
Create Date: 2021-04-04 17:12:42.184574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4c13da96c0e'
down_revision = 'db7b344694d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('User', sa.Column('a', sa.Float(), nullable=True), schema='twitter')
    op.add_column('User', sa.Column('c', sa.Float(), nullable=True), schema='twitter')
    op.add_column('User', sa.Column('e', sa.Float(), nullable=True), schema='twitter')
    op.add_column('User', sa.Column('n', sa.Float(), nullable=True), schema='twitter')
    op.add_column('User', sa.Column('o', sa.Float(), nullable=True), schema='twitter')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('User', 'o', schema='twitter')
    op.drop_column('User', 'n', schema='twitter')
    op.drop_column('User', 'e', schema='twitter')
    op.drop_column('User', 'c', schema='twitter')
    op.drop_column('User', 'a', schema='twitter')
    # ### end Alembic commands ###
