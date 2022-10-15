"""Added RECALLED values to InviteStatus

Revision ID: c88acc2d573d
Revises: 604d7420855b
Create Date: 2022-10-15 12:32:17.927140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c88acc2d573d'
down_revision = '604d7420855b'
branch_labels = None
depends_on = None


def upgrade():
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE invitestatus ADD VALUE 'RECALLED'")


def downgrade():
    op.execute("ALTER TYPE invitestatus RENAME TO status_old")
    op.execute("CREATE TYPE invitestatus AS ENUM('CREATED', 'ACCEPTED', 'DECLINED', 'OUTDATED')")
    op.execute("ALTER TABLE event_invites ALTER COLUMN status drop default")
    op.execute("ALTER TABLE friend_invites ALTER COLUMN status drop default")
    op.execute((
        "ALTER TABLE event_invites ALTER COLUMN status TYPE invitestatus USING "
        "status::text::invitestatus"
    ))
    op.execute((
        "ALTER TABLE friend_invites ALTER COLUMN status TYPE invitestatus USING "
        "status::text::invitestatus"
    ))
    op.execute("DROP TYPE status_old")
