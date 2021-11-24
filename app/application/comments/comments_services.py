from abc import ABC

from fastapi import HTTPException, status

from app.domain.comments.entities.comments import CommentCreate
from app.domain.comments.interfaces.comment_repo import ICommentRepo


class CommentsService(ABC):
    """
    Comments Service
    """

    @classmethod
    def create_comment(
        cls,
        comment_repo: ICommentRepo,
        user_id: int,
        post_id: int,
        comment_data: CommentCreate,
    ):
        """
        Create a comment

        :param comment_repo: Comment Repository dependency
        :param user_id: User ID
        :param post_id: Post ID
        :param comment_data: Comment data
        :return: Comment
        """
        try:
            new_comment = comment_repo.create_comment(user_id, post_id, comment_data)

        except (ValueError, AttributeError, TypeError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
        return new_comment
