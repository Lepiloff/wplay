"""Add unique constraint to event_invites

Revision ID: 9ffd8bbf0692
Revises: c88acc2d573d
Create Date: 2022-10-17 16:41:15.390223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ffd8bbf0692'
down_revision = 'c88acc2d573d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint('unique_event_invites', 'event_invites', ['from_user', 'to_user', 'to_event'])


def downgrade():
    op.drop_constraint('unique_event_invites', 'event_invites', type_='unique')

