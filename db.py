import os
from decouple import config
import databases
import sqlalchemy


DEFAULT_DATABASE_URL = f"postgresql://{config('DB_USER')}:{config('DB_PASS')}" \
                       f"@{config('DB_HOST')}:5432/{config('DB_NAME')}"
DATABASE_URL = (os.getenv('DATABASE_URL', DEFAULT_DATABASE_URL))

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
