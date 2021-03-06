"""Station Update to SI3

Revision ID: 4d3fe3d7bdfd
Revises: 177aa1fdf479
Create Date: 2015-05-30 14:15:02.851313

"""

# revision identifiers, used by Alembic.
revision = '4d3fe3d7bdfd'
down_revision = '177aa1fdf479'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('station', sa.Column('city', sa.String(length=255), nullable=True))
    op.add_column('station', sa.Column('default_language', sa.String(length=5), nullable=True))
    op.add_column('station', sa.Column('keywords', sa.String(length=255), nullable=True))
    op.add_column('station', sa.Column('location_country', sa.String(length=5), nullable=True))
    op.add_column('station', sa.Column('phone_number', sa.String(length=128), nullable=True))
    op.add_column('station', sa.Column('postal_name', sa.String(length=255), nullable=True))
    op.add_column('station', sa.Column('sms_body', sa.String(length=255), nullable=True))
    op.add_column('station', sa.Column('sms_description', sa.String(length=255), nullable=True))
    op.add_column('station', sa.Column('sms_number', sa.String(length=128), nullable=True))
    op.add_column('station', sa.Column('street', sa.String(length=255), nullable=True))
    op.add_column('station', sa.Column('zipcode', sa.String(length=25), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('station', 'zipcode')
    op.drop_column('station', 'street')
    op.drop_column('station', 'sms_number')
    op.drop_column('station', 'sms_description')
    op.drop_column('station', 'sms_body')
    op.drop_column('station', 'postal_name')
    op.drop_column('station', 'phone_number')
    op.drop_column('station', 'location_country')
    op.drop_column('station', 'keywords')
    op.drop_column('station', 'default_language')
    op.drop_column('station', 'city')
    ### end Alembic commands ###
