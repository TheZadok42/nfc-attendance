from datetime import datetime

import sqlalchemy.orm

from nfc_attendence.dal.base import Base
from nfc_attendence.dal.group import Group


class Attendee(Base):
    __tablename__ = "attendees"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    group_id = sqlalchemy.Column(sqlalchemy.ForeignKey(Group.id), nullable=False)
    name = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    nfc_id = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    creation_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow)

    group = sqlalchemy.orm.relationship("Group", back_populates="attendees")
    attendances = sqlalchemy.orm.relationship("Attendance", back_populates="attendee")
