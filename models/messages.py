import enum

from sqlalchemy import Table, Column, Integer, Boolean, \
    ForeignKey, DateTime, sql, Text

from db import metadata
from .users import users


messages = Table(
    "messages",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("content", Text(), nullable=False),
    Column("sender", ForeignKey(users.c.id, ondelete="SET NULL"), nullable=False),
    Column("recipient", ForeignKey(users.c.id, ondelete="SET NULL"), nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=sql.func.now()),
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
