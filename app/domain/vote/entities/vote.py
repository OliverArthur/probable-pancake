from enum import Enum

from pydantic import BaseModel


class VoteType(int, Enum):
    UP: int = 1
    DOWN: int = 0


class VoteBase(BaseModel):
    post_id: int
    direction: VoteType


class VoteCreate(VoteBase):
    pass


class Vote(VoteBase):
    class Config:
        orm_mode = True
