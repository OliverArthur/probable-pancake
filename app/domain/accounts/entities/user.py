from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

pass_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"


# Shared properties
class UserBase(BaseModel):
    id: int
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow())


# Properties to receive on user creation via API
class UserCredentials(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128, regex=pass_regex)


class UserUpdateMe(BaseModel):
    full_name: Optional[str] = None


# Properties to push to user details via API
class User(UserBase):
    id: int
    update_at: Optional[datetime] = Field(default_factory=datetime.utcnow())

    class Config:
        allow_mutation = False
        orm_mode = True
