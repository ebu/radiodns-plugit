"""Added station_id

Revision ID: 41808ec16aa1
Revises: 485001e8d1b3
Create Date: 2013-08-19 15:48:35.069000

"""

# revision identifiers, used by Alembic.
revision = '41808ec16aa1'
down_revision = '485001e8d1b3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('show', sa.Column('station_id', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('show', 'station_id')
    ### end Alembic commands ###
