from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.domain.accounts.entities.user import User


class CommentBase(BaseModel):
    post_id: int
    body: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    commented_by: Optional[User] = None
    created_at: Optional[datetime] = datetime.utcnow()
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class CommentUpdate(CommentBase):
    body: Optional[str] = None
