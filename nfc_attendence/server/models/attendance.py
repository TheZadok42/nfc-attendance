from datetime import datetime

from pydantic import BaseModel

from nfc_attendence.server.models.attendee import Attendee
from nfc_attendence.server.models.check_point import CheckPoint


class CreateAttendance(BaseModel):
    attendee_id: int
    check_point_id: int


class Attendance(CreateAttendance):
    id: int
    creation_date: datetime

    check_point: CheckPoint
    attendee: Attendee

    class Config:
        orm_mode = True
