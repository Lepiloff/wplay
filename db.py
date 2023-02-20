import os
import databases
import sqlalchemy


DEFAULT_DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}" \
                       f"@{os.getenv('DB_HOST')}:5432/{os.getenv('DB_NAME')}"
DATABASE_URL = (os.getenv('DATABASE_URL', DEFAULT_DATABASE_URL))

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)