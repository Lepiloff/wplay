"""Added start_date field as date type

Revision ID: c36fa8066abe
Revises: f041b37ef445
Create Date: 2021-07-15 10:20:48.969353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c36fa8066abe'
down_revision = 'f041b37ef445'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('start_date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'start_date')
    # ### end Alembic commands ###