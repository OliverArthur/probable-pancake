from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.domain.accounts.entities.user import User


class PostsBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None


class PostsCreate(PostsBase):
    title: str
    content: str


class PostsUpdate(PostsBase):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None


class PostsPublished(PostsBase):
    id: int
    published: bool


class Posts(PostsBase):
    id: int
    created_at: Optional[datetime] = Field(None, alias="created_at")
    updated_at: Optional[datetime] = Field(None, alias="updated_at")
    published: bool = False
    owner: Optional[User] = None

    class Config:
        orm_mode = True


class PostsInDBOut(BaseModel):
    Posts: Posts
    votes: int

    class Config:
        orm_mode = True
