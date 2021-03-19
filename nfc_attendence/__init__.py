import sqlalchemy
from sqlalchemy.orm.session import sessionmaker

from nfc_attendence.dal import Base

conn_string = 'sqlite:///A:\\Dev\\nfc-attendance\\test.sqlite3'
engine = sqlalchemy.create_engine(conn_string)
Base.metadata.create_all(engine)

SessionBase = sessionmaker(engine)
