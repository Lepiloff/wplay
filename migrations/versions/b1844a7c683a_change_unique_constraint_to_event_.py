"""Change unique constraint to event_invites

Revision ID: b1844a7c683a
Revises: 9ffd8bbf0692
Create Date: 2022-10-17 17:11:14.732235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1844a7c683a'
down_revision = '9ffd8bbf0692'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('unique_event_invites', 'event_invites', type_='unique')
    op.create_unique_constraint('unique_event_invites', 'event_invites', ['from_user', 'to_user', 'to_event', 'is_active'])


def downgrade():
    op.drop_constraint('unique_event_invites', 'event_invites', type_='unique')
    op.create_unique_constraint('unique_event_invites', 'event_invites', ['from_user', 'to_user', 'to_event'])
