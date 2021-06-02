"""Added enum field to friend-invite table

Revision ID: bd7d4d57d23b
Revises: cbf9c9f4f218
Create Date: 2021-05-31 22:55:30.369891

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'bd7d4d57d23b'
down_revision = 'cbf9c9f4f218'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    invite_status = postgresql.ENUM('CREATED', 'ACCEPTED', 'DECLINED', 'OUTDATED', name='invite_status')
    invite_status.create(op.get_bind())
    op.add_column('friend_invites', sa.Column('status', sa.Enum('CREATED', 'ACCEPTED', 'DECLINED', 'OUTDATED', name='invite_status'), server_default='CREATED', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('friend_invites', 'status')
    invite_status = postgresql.ENUM('CREATED', 'ACCEPTED', 'DECLINED', 'OUTDATED', name='invite_status')
    op.drop_column('friend_invites', 'status')
    # ### end Alembic commands ###
