from datetime import datetime
from typing import List

from fastapi import APIRouter
from sqlalchemy.sql.elements import between
from sqlalchemy.sql.expression import select

from ..dal.models import Attendee
from ..dal.tables import attendance, attendees, engine

router = APIRouter(tags=['attendace'])


class AttendanceInstance(Attendee):
    insertion_time: datetime


@router.get('/attendance', response_model=List[AttendanceInstance])
async def receive_report(start_time: datetime, end_time: datetime = None):
    end_time = end_time or datetime.now()
    with engine.connect() as connection:
        action = select(
            attendees,
            attendance.c.insertion_time).select_from(attendance).join(
                attendees, attendees.c.id == attendance.c.attendee).where(
                    between(attendance.c.insertion_time, start_time, end_time))
        result = connection.execute(action)
        return [AttendanceInstance.parse_obj(item) for item in result]
