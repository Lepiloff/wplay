from sqlalchemy import Table, Column, Integer, Float, String, UniqueConstraint

from db import metadata


locations = Table(
    "locations",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("lat", Float(), nullable=False),
    Column("long", Float(), nullable=False),
    Column("city", String(100), nullable=False, index=True),
    Column("street", String(100), nullable=False),
    Column("building", String(10), nullable=False),
    UniqueConstraint("city", "street", "building", name="address")
)
