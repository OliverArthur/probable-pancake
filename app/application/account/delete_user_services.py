from fastapi import HTTPException, status

from app.domain.accounts.protocols.user_repo import UserRepo


class DeleteUserServices:
    @staticmethod
    async def delete_user(
        user_repo: UserRepo,
        user_id: int
    ) -> None:
        user = await user_repo.fetch(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        await user_repo.delete_one(user_id)
