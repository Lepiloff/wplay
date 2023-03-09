"""user active false

Revision ID: bd10050db684
Revises: 016912c0b14a
Create Date: 2023-03-09 20:42:39.174330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd10050db684'
down_revision = '016912c0b14a'
branch_labels = None
depends_on = None


def upgrade():
    # Modify the default value of the 'is_active' column to False
    op.alter_column('users', 'is_active', server_default=sa.sql.expression.false())

def downgrade():
    # Modify the default value of the 'is_active' column back to True
    op.alter_column('users', 'is_active', server_default=sa.sql.expression.true())

