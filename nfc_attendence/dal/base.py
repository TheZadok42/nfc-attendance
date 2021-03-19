from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import as_declarative


# Base = declarative_base()

@as_declarative()
class Base:
    pass


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, _connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
