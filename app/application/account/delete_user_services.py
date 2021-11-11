from fastapi import HTTPException, status

from app.domain.accounts.interfaces.user_repo import IUserRepo


class DeleteUserServices:
    @staticmethod
    def delete_user(user_repo: IUserRepo, user_id: int) -> None:
        user = user_repo.fetch(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        user_repo.delete_one(user_id)
