from datetime import datetime

import sqlalchemy.orm

from nfc_attendence.dal.base import Base


class CheckPoint(Base):
    __tablename__ = "checkpoints"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    creation_time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow)

    attendances = sqlalchemy.orm.relationship("Attendance", back_populates="check_point")
