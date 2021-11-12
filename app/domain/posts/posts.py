from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.domain.accounts.entities import User


class PostBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None
    published: bool = False


class PostCreate(PostBase):
    title: str
    content: str


class PostPublished(PostBase):
    id: int
    published: bool


class Post(PostBase):
    id: int
    owner: Optional[User] = None
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

    class Config:
        orm_mode = True
