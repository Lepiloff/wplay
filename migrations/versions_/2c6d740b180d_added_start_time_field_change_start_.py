"""Added start_time field, change start_date field type

Revision ID: 2c6d740b180d
Revises: e7c0b85fe40d
Create Date: 2021-07-15 10:16:10.798285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c6d740b180d'
down_revision = 'e7c0b85fe40d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('start_time', sa.Time(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'start_time')
    # ### end Alembic commands ###