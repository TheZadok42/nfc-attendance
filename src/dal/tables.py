from sqlalchemy import (Column, DateTime, ForeignKey, Integer, MetaData,
                        String, Table, create_engine)
from sqlalchemy.sql import func

engine = create_engine('sqlite:///./test.db', echo=True)
metadata = MetaData(bind=engine)

events = Table(
    'events',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    # TODO: unique constarint
    Column('name', String, nullable=False),
    Column('start', DateTime, nullable=False, server_default=func.now()),
    Column('end', DateTime),
)

attendees = Table(
    'attendees',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('nfc_id', String, primary_key=True, nullable=False),
    Column('first_name', String, nullable=False),
    Column('last_name', String, nullable=False),
)

attendance = Table(
    'attendance',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('insertion_time', DateTime, server_default=func.now()),
    Column('attendee', None, ForeignKey('attendees.id')),
)
