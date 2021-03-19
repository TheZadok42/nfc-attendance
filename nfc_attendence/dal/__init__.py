import sqlalchemy
from sqlalchemy.orm import sessionmaker

from .attendance import Attendance
from .attendee import Attendee
from .base import Base
from .check_point import CheckPoint
from .group import Group


def get_engine(uri=None):
    return sqlalchemy.create_engine(f"sqlite:///{uri or ''}", connect_args={"check_same_thread": False})


def get_session_base(engine):
    session_base = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    try:
        yield session_base
    finally:
        pass


def get_session(session_base):
    session = session_base()
    try:
        yield session
    finally:
        session.close()
