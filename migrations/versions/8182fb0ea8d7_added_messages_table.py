"""Added messages table

Revision ID: 8182fb0ea8d7
Revises: 119d680d253a
Create Date: 2021-06-01 11:28:24.219152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8182fb0ea8d7'
down_revision = '119d680d253a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('sender', sa.Integer(), nullable=False),
    sa.Column('recipient', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('is_read', sa.Boolean(), server_default=sa.text('false'), nullable=True),
    sa.Column('trash', sa.Boolean(), server_default=sa.text('false'), nullable=True),
    sa.ForeignKeyConstraint(['recipient'], ['users.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['sender'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    # ### end Alembic commands ###
