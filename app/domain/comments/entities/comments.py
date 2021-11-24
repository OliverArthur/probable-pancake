from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CommentBase(BaseModel):
    user_id: int
    post_id: int
    body: Optional[str] = None


class CommentCreate(CommentBase):
    body: str


class Comment(CommentBase):
    id: int
    created_at: Optional[datetime] = datetime.utcnow()
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class CommentUpdate(CommentBase):
    body: Optional[str] = None
