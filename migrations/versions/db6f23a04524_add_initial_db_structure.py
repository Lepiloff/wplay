"""Add initial db structure

Revision ID: db6f23a04524
Revises: 
Create Date: 2021-03-02 00:30:43.239666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db6f23a04524'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('activities_level',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('level', sa.Enum('BASIC', 'MEDIUM', 'ADVANCED', 'PROFESSIONAL', name='activitieslevel'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lat', sa.Float(), nullable=False),
    sa.Column('long', sa.Float(), nullable=False),
    sa.Column('city', sa.String(length=100), nullable=False),
    sa.Column('street', sa.String(length=100), nullable=False),
    sa.Column('building', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('city', 'street', 'building', name='address')
    )
    op.create_index(op.f('ix_locations_city'), 'locations', ['city'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('email', sa.String(length=40), nullable=False),
    sa.Column('phone', sa.String(length=16), nullable=False),
    sa.Column('hashed_password', sa.String(length=256), nullable=True),
    sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('account_activities_level',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=False),
    sa.Column('activity_id', sa.Integer(), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['level'], ['activities_level.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=16), nullable=False),
    sa.Column('surname', sa.String(length=16), nullable=False),
    sa.Column('age', sa.String(length=3), nullable=True),
    sa.Column('personal_info', sa.Text(), nullable=True),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', name='gender'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creator', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('status', sa.Enum('OPEN', 'CLOSED', 'EXPIRE', name='status'), server_default='OPEN', nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=True),
    sa.Column('is_group', sa.Boolean(), server_default=sa.text('true'), nullable=True),
    sa.Column('is_private', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.Column('activities_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['activities_id'], ['activities.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['creator'], ['users.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('location_id', 'id', name='event_location')
    )
    op.create_table('friends',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_one_id', sa.Integer(), nullable=False),
    sa.Column('user_two_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_one_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_two_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_one_id', 'user_two_id', name='buddy')
    )
    op.create_table('event_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('events_id', sa.Integer(), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['events_id'], ['events.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feedbacks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('reason', sa.Text(), nullable=True),
    sa.Column('is_negative', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('from_user', sa.Integer(), nullable=False),
    sa.Column('to_user', sa.Integer(), nullable=False),
    sa.Column('to_event', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['from_user'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['to_event'], ['events.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['to_user'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feedbacks')
    op.drop_table('event_users')
    op.drop_table('friends')
    op.drop_table('events')
    op.drop_table('accounts')
    op.drop_table('account_activities_level')
    op.drop_table('users')
    op.drop_index(op.f('ix_locations_city'), table_name='locations')
    op.drop_table('locations')
    op.drop_table('activities_level')
    op.drop_table('activities')
    # ### end Alembic commands ###
