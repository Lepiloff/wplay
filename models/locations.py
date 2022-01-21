from sqlalchemy import Table, Column, Integer, Float, String, UniqueConstraint

from db import metadata


locations = Table(
    "locations",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("lat", Float(), nullable=False),
    Column("long", Float(), nullable=False),
    Column("country", String(20), nullable=False),
    Column("city", String(20), nullable=False, index=True),
    Column("street", String(20), nullable=False),
    Column("building", String(5), nullable=False),
    UniqueConstraint("city", "street", "building", name="address")
)
