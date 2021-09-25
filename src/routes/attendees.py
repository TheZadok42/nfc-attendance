from operator import and_
from typing import List, Optional

from fastapi import APIRouter
from sqlalchemy.sql.expression import select

from ..dal.models import Attendee, BaseAttendee, NFCCard
from ..dal.tables import attendees, engine, nfc_cards
from ..wrappers import NFCWrapper, ScreenWrapper

router = APIRouter(tags=['attendees'])
screen = ScreenWrapper()
nfc = NFCWrapper()

screen.setup()
nfc.setup()

# TODO: attendees
# 1. Better setup


def _get_nfc_tag_uid():
    uid = nfc.get_uid()
    while uid is None:
        uid = nfc.get_uid()


def _get_nfc_tag_record(uid: str) -> NFCCard:
    with engine.connect() as connection:
        result = connection.execute(
            nfc_cards.select().where(nfc_cards.c.uid == uid))
        card = result.fetchone()
        if card:
            return NFCCard.parse_obj(card)
        else:
            result = connection.execute(nfc_cards.insert().values(uid=uid))
            id = result.inserted_primary_key[0]
            return NFCCard(uid=uid, id=id)


def _get_attendee_by_card(card: NFCCard) -> Optional[Attendee]:
    with engine.connect() as connection:
        result = connection.execute(
            attendees.select(
                and_(attendees.c.nfc_id == card.id,
                     attendees.c.active == True)))
        return result.fetchone()


def _get_nfc_tag(attendee: BaseAttendee) -> NFCCard:
    uid = _get_nfc_tag_uid()
    card = _get_nfc_tag_record(uid)
    current_attendee = _get_attendee_by_card(card)
    if current_attendee:
        screen.write(
            f'The nfc card is used by '
            f'{current_attendee.first_name} {current_attendee.last_name}, '
            'try a diffrent card')
        return _get_nfc_tag(attendee)
    screen.write(f'{attendee.first_name} is registered')
    return card


def _handle_new_attendees(new_attendees: List[BaseAttendee]):
    for attendee in new_attendees:
        screen.write(f'Register {attendee.first_name}\'s nfc card')
        yield Attendee(**attendee.dict(), nfc_id=_get_nfc_tag(attendee).id)


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


@router.get('/attendees/nfc', response_model=Attendee)
async def get_attendee_by_card():
    screen.write('Press the atendee\'s card')
    uid = _get_nfc_tag_uid()
    card = _get_nfc_tag_record(uid)
    return _get_attendee_by_card(card)


@router.delete('/attendees', response_model=Attendee)
async def deactivate_attendee():
    screen.write('Press the atendee\'s card')
    uid = _get_nfc_tag_uid()
    card = _get_nfc_tag_record(uid)
    attendee = _get_attendee_by_card(card)
    with engine.connect() as connection:
        connection.execute(attendees.update().where(
            attendees.c.id == attendee.id).values(active=False))
    attendee.active = False
    return attendee
