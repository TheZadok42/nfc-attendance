from fastapi import FastAPI

from models.group import Group, CreateGroup
from nfc_attendence import dal

db_engine = dal.get_engine()
session_base = dal.get_session_base(db_engine)
dal.Base.metadata.create_all(db_engine)

app = FastAPI()


@app.post("/groups", response_model=Group)
async def create_group(group: CreateGroup):
    session = dal.get_session(session_base)
    db_group = dal.Group(name=group.name, description=group.description)
    session.add(db_group)
    session.commit()
    session.refresh(db_group)
    return db_group
