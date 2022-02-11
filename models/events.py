import enum

from sqlalchemy import Table, Column, Integer, Boolean, Date, Time, Text, String, \
    ForeignKey, DateTime, sql, UniqueConstraint, Enum

from db import metadata
from helpers.utils import EnumAsInteger
from models.locations import locations
from models.activities import activities
from models.users import users


class MembersQuantity(enum.Enum):
    two = '2'
    three = '3'
    four = '4'
    five = '5'
    six = '6'
    seven = '7'
    eight = '8'
    nine = '9'
    ten = '10'
    eleven = '11'
    twelve = '12'
    thirteen = '13'
    fourteen = '14'
    fifteen = '15'
    sixteen = '16'
    seventeen = '17'
    eighteen = '18'
    nineteen = '19'
    twenty = '20'
    thirty = '30'
    forty = '40'
    fifty = '50'
    unlimited = '1000'


class Status(enum.Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    EXPIRE = "EXPIRE"


events = Table(
    "events",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("creator", ForeignKey(users.c.id, ondelete="SET NULL"), nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=sql.func.now()),
    Column("title", String(100), nullable=False),
    Column("content", Text(), nullable=False),
    Column("start_date", Date()),
    Column("start_time", Time()),
    Column("status", Enum(Status, values_callable=lambda obj: [e.value for e in obj]),
           nullable=False,
           default=Status.OPEN.value,
           server_default=Status.OPEN.value),
    Column(
        "is_active",
        Boolean(),
        server_default=sql.expression.true(),
        nullable=True,
    ),
    Column("members_count", EnumAsInteger(MembersQuantity),
           nullable=False,
           default=MembersQuantity.two.value,
           server_default=MembersQuantity.two.value),
    Column(
        "is_private",
        Boolean(),
        server_default=sql.expression.true(),
        nullable=False,
    ),
    Column("location_id", ForeignKey(locations.c.id, ondelete="SET NULL"), nullable=False),
    Column("activities_id", ForeignKey(activities.c.id, ondelete="SET NULL"), nullable=False),
    UniqueConstraint("location_id", "id", name="event_location")
)

event_users = Table(
    "event_users",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("events_id", ForeignKey(events.c.id, ondelete="SET NULL"), nullable=False),
    Column("users_id", ForeignKey(users.c.id, ondelete="SET NULL"), nullable=False),
    UniqueConstraint("events_id", "users_id", name="events_user")
)
