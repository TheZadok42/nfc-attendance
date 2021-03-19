from datetime import datetime

import sqlalchemy.orm

from nfc_attendence.dal.base import Base


class Group(Base):
    __tablename__ = 'groups'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    creation_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow)

    attendees = sqlalchemy.orm.relationship("Attendee", back_populates='group')
