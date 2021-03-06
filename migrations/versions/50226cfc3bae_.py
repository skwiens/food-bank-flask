"""empty message

Revision ID: 50226cfc3bae
Revises: 1b6ab5093880
Create Date: 2018-01-17 21:46:32.990377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50226cfc3bae'
down_revision = '1b6ab5093880'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('volunteer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('role', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('openhour_shoppers',
    sa.Column('openhour_id', sa.Integer(), nullable=True),
    sa.Column('volunteer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['openhour_id'], ['openhour.id'], ),
    sa.ForeignKeyConstraint(['volunteer_id'], ['volunteer.id'], )
    )
    op.create_table('openhour_volunteers',
    sa.Column('openhour_id', sa.Integer(), nullable=True),
    sa.Column('volunteer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['openhour_id'], ['openhour.id'], ),
    sa.ForeignKeyConstraint(['volunteer_id'], ['volunteer.id'], )
    )
    op.drop_column('openhour', 'shoppers')
    op.drop_column('openhour', 'volunteers')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('openhour', sa.Column('volunteers', sa.VARCHAR(length=255), nullable=True))
    op.add_column('openhour', sa.Column('shoppers', sa.VARCHAR(length=255), nullable=True))
    op.drop_table('openhour_volunteers')
    op.drop_table('openhour_shoppers')
    op.drop_table('volunteer')
    # ### end Alembic commands ###
