from os import environ
import sys

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context


sys.path = ['', '..'] + sys.path[1:]

config = context.config


from db import metadata

from models.events import event_users, events
from models.locations import locations
from models.activities import activities, activities_level, account_activities_level
from models.feedbacks import feedbacks
from models.users import users, accounts, friends
from models.invites import event_invites, friend_invites
from models.notifications import notifications
from models.messages import messages

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = metadata

section = config.config_ini_section
config.set_section_option(section, "DB_USER", environ.get("DB_USER"))
config.set_section_option(section, "DB_PASS", environ.get("DB_PASS"))
config.set_section_option(section, "DB_NAME", environ.get("DB_NAME"))
config.set_section_option(section, "DB_HOST", environ.get("DB_HOST"))

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run _migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run _migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
