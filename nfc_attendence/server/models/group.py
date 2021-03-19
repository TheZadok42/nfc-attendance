from datetime import datetime

from pydantic import BaseModel


class CreateGroup(BaseModel):
    name: str
    description: str


class Group(CreateGroup):
    id: int
    creation_date: datetime

    class Config:
        orm_mode = True
