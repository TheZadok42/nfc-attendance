from datetime import datetime

import sqlalchemy.orm

from nfc_attendence.dal.attendee import Attendee
from nfc_attendence.dal.base import Base
from nfc_attendence.dal.check_point import CheckPoint


class Attendance(Base):
    __tablename__ = "attendance"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    attendee_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Attendee.id), nullable=False)
    check_point_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(CheckPoint.id), nullable=False)
    creation_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow)

    check_point = sqlalchemy.orm.relationship("CheckPoint", back_populates="attendances")
    attendee = sqlalchemy.orm.relationship("Attendee", back_populates="attendances")
