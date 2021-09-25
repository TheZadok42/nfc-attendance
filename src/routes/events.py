from datetime import datetime
from operator import and_
from typing import List, Optional

from fastapi import APIRouter
from sqlalchemy.sql.elements import between
from sqlalchemy.sql.expression import select
from src.dal.models import Attendee, BaseEvent, Event
from src.dal.tables import attendance, attendees, engine, events

router = APIRouter(tags=['events'])


class UpdateEvent(BaseEvent):
    name: Optional[str]


class AttendeesEvent(Event):
    attendees: List[Attendee]


def _get_event(id: Optional[int] = None, name: Optional[str] = None) -> Event:
    if id:
        where_clause = events.c.id == id
    elif name:
        where_clause = events.c.name == name
    with engine.connect() as connection:
        result = connection.execute(events.select().where(where_clause))
        return Event.parse_obj(result.fetchone())


@router.post('/event', response_model=Event)
async def save_new_event(event: BaseEvent):
    with engine.connect() as connection:
        result = connection.execute(events.insert(), **event.dict())
        inserted_primary_key = result.inserted_primary_key[0]
    return Event(id=inserted_primary_key, **event.dict())


@router.put('/event/{event_id}', response_model=Event)
async def update_event(event_id, event: UpdateEvent):
    where_condiction = events.c.id == event_id
    action = events.update().where(where_condiction).values(**event.dict(
        exclude_none=True))
    with engine.connect() as connection:
        connection.execute(action)
        result = connection.execute(events.select().where(where_condiction))
        updated_event = result.fetchone()
    return updated_event


@router.get('/event/all', response_model=List[Event])
async def get_event():
    with engine.connect() as connection:
        result = connection.execute(events.select())
        return result.fetchall()


@router.get('/event', response_model=Event)
async def get_event(id: Optional[int] = None, name: Optional[str] = None):
    return _get_event(id, name)


@router.get('/event/attendees', response_model=AttendeesEvent)
async def get_events_with_attendees(id: Optional[int] = None,
                                    name: Optional[str] = None):
    event = _get_event(id, name)
    with engine.connect() as connection:
        action = select([attendees]).select_from(attendance).join(
            attendees, attendance.c.attendee == attendees.c.id).where(
                between(attendance.c.insertion_time, event.start, event.end
                        or datetime.now()))
        result = connection.execute(action)
        event_attendees = result.fetchall()
    return AttendeesEvent(**event.dict(), attendees=event_attendees)
