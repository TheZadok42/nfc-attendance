from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseAttendee(BaseModel):
    id: int
    first_name: str
    last_name: str


class Attendee(BaseAttendee):
    nfc_id: str


class BaseEvent(BaseModel):
    name: str
    start: Optional[datetime]
    end: Optional[datetime]


class Event(BaseEvent):
    id: int
