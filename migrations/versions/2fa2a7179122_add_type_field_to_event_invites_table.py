"""Add type field to event_invites table

Revision ID: 2fa2a7179122
Revises: a6d5362d76e4
Create Date: 2021-04-04 16:31:00.051348

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2fa2a7179122'
down_revision = 'a6d5362d76e4'
branch_labels = None
depends_on = None


def upgrade():
    invitetype = postgresql.ENUM('INVITE', 'BET', name='invitetype')
    invitetype.create(op.get_bind())
    op.add_column('event_invites', sa.Column('type', sa.Enum('INVITE', 'BET', name='invitetype'), nullable=False))


def downgrade():
    op.drop_column('event_invites', 'type')
    invitetype = postgresql.ENUM('INVITE', 'BET', name='invitetype')
    invitetype.drop(op.get_bind())
