from fastapi import FastAPI

from models.group import Group, CreateGroup
from nfc_attendence import dal

app = FastAPI()


@app.post("/groups", response_model=Group)
async def create_group(group: CreateGroup):
    session = dal.SessionBase()
    db_group = dal.Group(name=group.name, description=group.description)
    session.add(db_group)
    session.commit()
    session.refresh(db_group)
    return db_group
