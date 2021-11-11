from typing import Protocol

from pydantic.networks import EmailStr

from app.domain.accounts.entities.user import User


class UserRepo(Protocol):
    async def create(self, email: EmailStr, password_hash: str) -> User:
        ...

    async def fetch(self, id: int) -> User:
        ...

    async def fetch_by_email(self, email: EmailStr) -> User:
        ...

    async def delete_one(self, id: int) -> None:
        ...

    async def update_one(self, id: int, email: EmailStr, password_hash: str) -> None:
        ...

    async def update_password(self, id: int, password_hash: str) -> None:
        ...
