from typing import List, Protocol

from app.domain.comments.entities.comments import Comment, CommentCreate, CommentUpdate


class ICommentRepo(Protocol):
    """
    Interface for comment repository.
    """

    async def get_comments(self, post_id: int) -> List[Comment]:
        ...

    async def get_comment(self, comment_id: int) -> Comment:
        ...

    async def create_comment(
        self, user_id: int, post_id: int, comment: CommentCreate
    ) -> Comment:
        ...

    async def update_comment(self, comment_id: int, comment: CommentUpdate) -> Comment:
        ...

    async def delete_comment(self, comment_id: int) -> dict:
        ...
