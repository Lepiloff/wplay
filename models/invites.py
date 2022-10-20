import enum

from sqlalchemy import Table, Column, Integer, Boolean, \
    ForeignKey, DateTime, sql, Enum, Index

from db import metadata
from .events import events
from .users import users


class InviteStatus(enum.Enum):
    CREATED = 'CREATED'
    ACCEPTED = 'ACCEPTED'
    DECLINED = 'DECLINED'
    OUTDATED = 'OUTDATED'
    RECALLED = 'RECALLED'


class InviteType(enum.Enum):
    INVITE = 'INVITE'
    BET = 'BET'


event_invites = Table(
    "event_invites",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("from_user", ForeignKey(users.c.id, ondelete="SET NULL"), nullable=False),
    Column("to_user", ForeignKey(users.c.id, ondelete="SET NULL"), nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=sql.func.now()),
    Column("to_event", ForeignKey(events.c.id, ondelete="CASCADE"), nullable=False),
    Column("status", Enum(InviteStatus, values_callable=lambda obj: [e.value for e in obj]),
           nullable=False,
           default=InviteStatus.CREATED.value,
           server_default=InviteStatus.CREATED.value),
    Column("type", Enum(InviteType, values_callable=lambda obj: [e.value for e in obj]),
           nullable=False),
    Column(
        "is_active",
        Boolean(),
        server_default=sql.expression.true(),
        nullable=True,
    ),
    Index("unique_event_invites", "from_user", "to_user", "to_event", "is_active", unique=True,
          postgresql_where=Column("is_active='True'"))
)


friend_invites = Table(
    "friend_invites",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("from_user", ForeignKey(users.c.id, ondelete="SET NULL"), nullable=False),
    Column("to_user", ForeignKey(users.c.id, ondelete="SET NULL"), nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=sql.func.now()),
    Column("status", Enum(InviteStatus, values_callable=lambda obj: [e.value for e in obj]),
           nullable=False,
           default=InviteStatus.CREATED.value,
           server_default=InviteStatus.CREATED.value),
)
