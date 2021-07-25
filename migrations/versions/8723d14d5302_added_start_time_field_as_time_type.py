"""Added start_time field as time type

Revision ID: 8723d14d5302
Revises: 74acbe81ec0f
Create Date: 2021-07-15 17:10:25.125074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8723d14d5302'
down_revision = '74acbe81ec0f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('start_time', sa.Time(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'start_time')
    # ### end Alembic commands ###
