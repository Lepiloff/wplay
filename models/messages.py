import enum

from sqlalchemy import Table, Column, Integer, Boolean, \
    ForeignKey, DateTime, sql, Text, Enum

from db import metadata
from .users import users
from models.events import events
from models.invites import event_invites


class NotificationType(enum.Enum):
    EVENT = 'EVENT'
    MESSAGE = 'MESSAGE'
    FRIENDSHIP = 'FRIENDSHIP'


Column("type", Enum(NotificationType, values_callable=lambda obj: [e.value for e in obj]),
       nullable=False),


messages = Table(
    "messages",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("content", Text(), nullable=False),
    Column("sender", ForeignKey(users.c.id, ondelete="SET NULL"), nullable=False),
    Column("event", ForeignKey(events.c.id, ondelete="SET NULL"), nullable=False),
    Column("event_invite", ForeignKey(event_invites.c.id, ondelete="SET NULL"), nullable=False),
    Column("recipient", ForeignKey(users.c.id, ondelete="SET NULL"), nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=sql.func.now()),
    Column("type", Enum(NotificationType, values_callable=lambda obj: [e.value for e in obj]),
           nullable=False),
    Column(
        "is_read",
        Boolean(),
        server_default=sql.expression.false(),
        nullable=True,
    ),
    Column(
        "trash",
        Boolean(),
        server_default=sql.expression.false(),
        nullable=True,
    ),
)
