from pydantic import BaseModel


class CreateAttendee(BaseModel):
    group_id: int
    name: int


class Attendee(CreateAttendee):
    from .group import Group
    id: int
    nfc_id: str
    creation_date: str

    group: Group

    class Config:
        orm_mode = True
