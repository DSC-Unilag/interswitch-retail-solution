"""empty message

Revision ID: a8776ebb2c16
Revises: 
Create Date: 2019-08-01 10:38:38.641783

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8776ebb2c16'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('producer', sa.Column('address', sa.String(length=225), nullable=True))
    op.create_unique_constraint(None, 'producer', ['address'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'producer', type_='unique')
    op.drop_column('producer', 'address')
    # ### end Alembic commands ###
