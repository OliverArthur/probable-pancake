from datetime import datetime

from typing import Optional
from pydantic import BaseModel


class TopicBase(BaseModel):
    title: str
    description: str


class TopicCreate(TopicBase):
    pass


class TopicUpdate(TopicBase):
    pass


class Topic(TopicBase):
    id: int
    created_at: Optional[datetime] = datetime.utcnow()
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
