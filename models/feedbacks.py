from sqlalchemy import Table, Column, Integer, Boolean, Text, ForeignKey, DateTime, sql

from db import metadata
from .users import users
from .events import events
    

feedbacks = Table(
    "feedbacks",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("created_at",  DateTime(timezone=True), server_default=sql.func.now()),
    Column("reason", Text()),
    Column(
        "is_negative",
        Boolean(),
        server_default=sql.expression.false(),
        nullable=False,
    ),
    Column("from_user", ForeignKey(users.c.id, ondelete="CASCADE"), nullable=False),
    Column("to_user", ForeignKey(users.c.id,  ondelete="CASCADE"), nullable=False),
    Column("to_event", ForeignKey(events.c.id, ondelete="SET NULL"), nullable=False),
)
