from __future__ import annotations

from typing import List

from fastapi import HTTPException, status

from app.domain.comments.entities.comments import Comment, CommentCreate
from app.infrastructure.database.models.comments import Comments as CommentModel
from app.infrastructure.database.sqlalchemy import db


def get_comments(
    post_id: int,
    page: int = 1,
    per_page: int = 10,
) -> List[Comment]:
    """
    Fetch comments by post id

    :param post_id: post id
    :param page: page number
    :param per_page: number of comments per page
    :return: list of comments
    """
    comments = (
        db.session.query(CommentModel)
        .filter(CommentModel.post_id == post_id)
        .limit(per_page)
        .offset((page - 1) * per_page)
    )

    if not comments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comments not found for this post",
        )

    return comments


def create_comment(post_id: int, user_id: int, comment: CommentCreate) -> Comment:
    """
    Create new comment

    :param post_id: post id
    :param user_id: user id
    :param comment: comment
    :return: comment
    """

    if comment.body is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Comment body is required",
        )

    comment = CommentModel(
        post_id=post_id,
        user_id=user_id,
        body=comment.body,
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment
