from sqlalchemy import (Column, DateTime, ForeignKey, Integer, MetaData,
                        String, Table, create_engine)
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Boolean

engine = create_engine('sqlite:///./test.db', echo=True)
metadata = MetaData(bind=engine)

events = Table(
    'events',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String, nullable=False),
    Column('start', DateTime, nullable=False, server_default=func.now()),
    Column('end', DateTime),
)

nfc_cards = Table(
    'nfc_cards',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('uid', String, primary_key=True, nullable=False),
)

attendees = Table(
    'attendees',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('nfc_id', None, ForeignKey('nfc_cards.id')),
    Column('first_name', String, nullable=False),
    Column('last_name', String, nullable=False),
    Column('active', Boolean, default=True),
)

attendance = Table(
    'attendance',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('insertion_time', DateTime, server_default=func.now()),
    Column('attendee', None, ForeignKey('attendees.id')),
)
