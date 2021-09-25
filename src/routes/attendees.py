from typing import List

from fastapi import APIRouter

from ..dal.models import Attendee, BaseAttendee
from ..dal.tables import attendees, engine
from ..wrappers import NFCWrapper, ScreenWrapper

router = APIRouter(tags=['attendees'])
screen = ScreenWrapper()
nfc = NFCWrapper()

screen.setup()
nfc.setup()


def _get_nfc_tag(attendee: BaseAttendee):
    screen.write(f'Register {attendee.first_name}\'s nfc card')
    uid = nfc.get_uid()
    while uid is None:
        uid = nfc.get_uid()
    screen.write(f'{attendee.first_name} nfc card\'s id is {uid}')
    return uid


def _handle_new_attendees(new_attendees: List[BaseAttendee]):
    for attendee in new_attendees:
        yield Attendee(**attendee.dict(), nfc_id=_get_nfc_tag(attendee))


@router.post('/attendees', response_model=List[Attendee])
async def register_attendees(new_attendees: List[BaseAttendee]):
    parsed_attendees = list(_handle_new_attendees(new_attendees))
    with engine.connect() as connection:
        connection.execute(attendees.insert(),
                           [attendee.dict() for attendee in parsed_attendees])
    return parsed_attendees


@router.get('/attendees', response_model=List[Attendee])
async def get_attendees():
    with engine.connect() as connection:
        result = connection.execute(attendees.select())
        return result.fetchall()
