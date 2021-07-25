import enum

from sqlalchemy import Table, Column, Integer, ForeignKey, Enum

from db import metadata
from .users import users


# NOT USING NOW
class NotificationStatus(enum.Enum):
    EVENT = 'EVENT'
    MESSAGE = 'MESSAGE'
    FRIENDSHIP = 'FRIENDSHIP'


Column("type", Enum(NotificationStatus, values_callable=lambda obj: [e.value for e in obj]),
       nullable=False),


notifications = Table(
    "notifications",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("recipient", ForeignKey(users.c.id, ondelete="CASCADE"), nullable=False),
    Column("type", Enum(NotificationStatus, values_callable=lambda obj: [e.value for e in obj]),
           nullable=False),
)

