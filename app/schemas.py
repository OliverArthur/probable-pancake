from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.networks import EmailStr


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    user_id: Optional[int] = None
    is_active: Optional[bool] = None


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False


class PostCreate(PostBase):
    title: str
    content: str


class PostUpdate(PostBase):
    title: Optional[str] = None
    content: Optional[str] = None


class PublishPost(BaseModel):
    id: int
    published: bool


class Post(PostBase):
    id: int
    created_at: Optional[datetime] = None
    owner: Optional[UserOut] = None

    class Config:
        orm_mode = True
