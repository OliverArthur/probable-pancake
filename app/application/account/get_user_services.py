from typing import Optional

from fastapi import HTTPException, status

from app.application.authentication.authentication_services import AuthenticationServices
from app.domain.accounts.entities.user import User, UserCredentials
from app.domain.accounts.protocols.user_repo import UserRepo


class GetUserServices:
    @staticmethod
    async def get_user_by_credentials(
        user_repo: UserRepo,
        user_credentials: UserCredentials,
    ) -> Optional[User]:

        user = await user_repo.fetch_by_email(user_credentials.email.lower())

        if not user:
            return None

        password = user_credentials.password
        password_hash = user.password_hash

        if not AuthenticationServices.verify_password(password, password_hash):
            return None

        return User(**user.dict())

    @staticmethod
    async def get_user_by_id(
        user_repo: UserRepo,
        user_id: int,
    ) -> Optional[User]:
        user = await user_repo.fetch(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return User(**user.dict())