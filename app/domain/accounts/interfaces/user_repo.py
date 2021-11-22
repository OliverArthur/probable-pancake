from typing import Protocol

from pydantic.networks import EmailStr

from app.domain.accounts.entities.user import User


class IUserRepo(Protocol):
    async def create(self, email: EmailStr, password_hash: str) -> User:
        ...

    async def fetch(self, id: int) -> User:
        ...

    async def fetch_by_email(self, email: EmailStr) -> User:
        ...

    async def update_password(self, id: int, password_hash: str) -> None:
        ...

    async def update_me(self, id: int, data: dict) -> None:
        ...