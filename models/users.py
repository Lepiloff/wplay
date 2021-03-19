import enum

from sqlalchemy import Table, Column, Integer, DateTime, Text, ForeignKey,\
     Enum, String, sql, Boolean, UniqueConstraint

from db import metadata


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", DateTime(timezone=True), server_default=sql.func.now()),
    Column("email", String(40), unique=True, nullable=False),
    Column("phone", String(16), unique=True, nullable=False),
    Column("hashed_password", String(256)),
    Column(
        "is_active",
        Boolean(),
        server_default=sql.expression.true(),
        nullable=True,
    ),
)


class Gender(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


accounts = Table(
    "accounts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(16), nullable=False),
    Column("surname", String(16), nullable=False),
    Column("age", String(3)),
    Column("personal_info", Text()),
    Column("gender", Enum(Gender, values_callable=lambda obj: [e.value for e in obj])),
    Column("user_id", ForeignKey(users.c.id, ondelete="CASCADE"), nullable=False),

)


friends = Table(
    "friends",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", DateTime(timezone=True), server_default=sql.func.now()),
    Column("user_one_id", ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("user_two_id", ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    UniqueConstraint("user_one_id", "user_two_id", name="buddy")
)


