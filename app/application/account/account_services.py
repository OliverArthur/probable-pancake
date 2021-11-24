from abc import ABC
from typing import Optional

from fastapi import HTTPException, status

from app.application.authentication.authentication_services import \
    AuthenticationServices
from app.domain.accounts.entities.user import (User, UserCredentials,
                                               UserUpdateMe)
from app.domain.accounts.interfaces.user_repo import IUserRepo


class AccountServices(ABC):
    @classmethod
    def get_user_by_id(cls, user_repo: IUserRepo, user_id: int) -> User:
        try:

            user = user_repo.fetch(user_id)

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with id: {user_id} not found",
                )

        except (AttributeError, ValueError, TypeError, Exception) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )

        return user

    @classmethod
    def verify_user_by_credentials(
        cls,
        user_repo: IUserRepo,
        user_credentials: UserCredentials,
    ) -> Optional[User]:
        user = user_repo.fetch_by_email(user_credentials.email.lower())

        try:

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )

            password = user_credentials.password
            password_hash = user.password

            if not AuthenticationServices.verify_password(password, password_hash):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials",
                )

        except (AttributeError, ValueError, TypeError, Exception) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )

        return user

    @classmethod
    def get_me(
        cls,
        user_repo: IUserRepo,
        current_user: UserCredentials,
    ) -> User:

        user = user_repo.fetch_by_email(current_user.email.lower())

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"We couldn't find a user with email: {user}",
            )

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
    def delete_user(cls, user_repo: IUserRepo, user_id: int) -> None:
        user = user_repo.fetch(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        user_repo.delete_one(user_id)

    @classmethod
    def update_me(
        cls,
        user_repo: IUserRepo,
        user_data: UserUpdateMe,
        user_credentials: UserCredentials,
    ) -> User:
        user = user_repo.fetch_by_email(user_credentials.email.lower())

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        user = user_repo.update_me(user, user_data)

        return user
