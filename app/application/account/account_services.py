from abc import ABC
from typing import Optional

from fastapi import HTTPException, status

from app.application.authentication.authentication_services import AuthenticationServices
from app.domain.accounts.entities.user import User, UserCredentials
from app.domain.accounts.interfaces.user_repo import IUserRepo


class AccountServices(ABC):
    @classmethod
    def get_user_by_id(cls, user_repo: IUserRepo, user_id: int) -> User:
        user = user_repo.fetch(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id: {user_id} not found",
            )

        return user

    @classmethod
    def get_user_by_credentials(
        cls,
        user_repo: IUserRepo,
        user_credentials: UserCredentials,
    ) -> Optional[User]:
        user = user_repo.fetch_by_email(user_credentials.email.lower())

        if not user:
            return None

        password = user_credentials.password
        password_hash = user.password

        if not AuthenticationServices.verify_password(password, password_hash):
            return None

        return user

    @classmethod
    def register_user(
        cls,
        user_repo: IUserRepo,
        user_credentials: UserCredentials,
    ) -> User:

        email = user_credentials.email.lower()
        user = user_repo.fetch_by_email(email)

        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists",
            )

        password_hash = AuthenticationServices.hash_password(user_credentials.password)

        user = user_repo.create(email, password_hash)

        return user

    @classmethod
    def update(
        cls,
        user_repo: IUserRepo,
        user_id: int,
        user_credentials: UserCredentials,
    ) -> User:
        user = user_repo.fetch(user_id)

        if not user:
            None

        email = user_credentials.email.lower()
        password_hash = AuthenticationServices.hash_password(user_credentials.password)

        user = user_repo.update(user_id, email, password_hash)

        return user

    @classmethod
    def delete_user(cls, user_repo: IUserRepo, user_id: int) -> None:
        user = user_repo.fetch(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        user_repo.delete_one(user_id)
