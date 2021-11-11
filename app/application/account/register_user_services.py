from fastapi import HTTPException, status

from app.application.authentication.authentication_services import (
    AuthenticationServices,
)
from app.domain.accounts.entities.user import User, UserCredentials
from app.domain.accounts.interfaces.user_repo import UserRepo


class RegisterUserServices:
    @staticmethod
    def register(
        user_repo: UserRepo,
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
