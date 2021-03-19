import sqlalchemy
from sqlalchemy.orm import sessionmaker

from .attendance import Attendance
from .attendee import Attendee
from .base import Base
from .check_point import CheckPoint
from .group import Group

conn_string = 'sqlite:///A:\\Dev\\nfc-attendance\\test.sqlite3'
engine = sqlalchemy.create_engine(conn_string)
Base.metadata.create_all(engine)

SessionBase = sessionmaker(engine)
