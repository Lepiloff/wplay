"""Updated event_invites table

Revision ID: a6d5362d76e4
Revises: d2803272bc0a
Create Date: 2021-04-04 15:19:48.139190

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a6d5362d76e4'
down_revision = 'd2803272bc0a'
branch_labels = None
depends_on = None


def upgrade():
    invitestatus = postgresql.ENUM('CREATED', 'ACCEPTED', 'DECLINED', 'OUTDATED', name='invitestatus')
    invitestatus.create(op.get_bind())
    op.add_column('event_invites', sa.Column('status', sa.Enum('CREATED', 'ACCEPTED', 'DECLINED', 'OUTDATED', name='invitestatus'), server_default='CREATED', nullable=False))


def downgrade():
    op.drop_column('event_invites', 'status')
    invitestatus = postgresql.ENUM('CREATED', 'ACCEPTED', 'DECLINED', 'OUTDATED', name='invitestatus')
    invitestatus.drop(op.get_bind())
