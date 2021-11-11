from fastapi import HTTPException, status

from app.application.authentication.authentication_services import (
    AuthenticationServices,
)
from app.domain.accounts.entities.user import User, UserCredentials
from app.domain.accounts.interfaces.user_repo import IUserRepo


class UpdateUserServices:
    @staticmethod
    def update(
        user_repo: IUserRepo,
        user_id: int,
        user_credentials: UserCredentials,
    ) -> User:
        user = user_repo.fetch(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        email = user_credentials.email.lower()
        password_hash = AuthenticationServices.hash_password(user_credentials.password)

        user = user_repo.update(user_id, email, password_hash)

        return user
