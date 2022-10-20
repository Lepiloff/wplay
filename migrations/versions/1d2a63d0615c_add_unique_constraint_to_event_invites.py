"""Add unique constraint to event_invites

Revision ID: 1d2a63d0615c
Revises: c88acc2d573d
Create Date: 2022-10-20 15:11:33.118903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d2a63d0615c'
down_revision = 'c88acc2d573d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('unique_event_invites', 'event_invites', ['from_user', 'to_user', 'to_event', 'is_active'], unique=True, postgresql_where=sa.text("is_active=True"))


def downgrade():
    op.drop_index('unique_event_invites', table_name='event_invites')
