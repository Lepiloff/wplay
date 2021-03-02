import enum

from sqlalchemy import Table, Column, Integer, Boolean, String, ForeignKey, Enum, sql

from db import metadata
from .users import users


class ActivitiesLevel(enum.Enum):
    BASIC = 'BASIC'
    MEDIUM = 'MEDIUM'
    ADVANCED = 'ADVANCED'
    PROFESSIONAL = 'PROFESSIONAL'


activities = Table(
    "activities",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("name", String(20)),
    Column(
        "is_active",
        Boolean(),
        server_default=sql.expression.true(),
        nullable=True,
    ),
)


activities_level = Table(
    'activities_level',
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("level", Enum(ActivitiesLevel, values_callable=lambda obj: [e.value for e in obj]),
           nullable=False),
)


account_activities_level = Table(
    "account_activities_level",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("users_id", ForeignKey(users.c.id, ondelete="CASCADE"), nullable=False),
    Column("activity_id", ForeignKey(activities.c.id, ondelete="CASCADE"), nullable=False),
    Column("level", ForeignKey(activities_level.c.id, ondelete="CASCADE"), nullable=False)
)
