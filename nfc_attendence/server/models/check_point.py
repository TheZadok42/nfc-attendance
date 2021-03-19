from typing import Optional

from pydantic import BaseModel


class CreateCheckpoint(BaseModel):
    description: Optional[str] = None


class CheckPoint(CreateCheckpoint):
    id: int
    creation_time: str

    class Config:
        orm_mode = True
