from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.sql import func

from app.domain.posts.entities.posts import Posts
from app.infrastructure.database.models.comments import \
    Comments as CommentsModel
from app.infrastructure.database.models.posts import Posts as PostsModel
from app.infrastructure.database.models.vote import Vote as VoteModel
from app.infrastructure.database.sqlalchemy import db


def fetch(post_id: int) -> Posts:
    post = (
        db.query(PostsModel, func.count(VoteModel.post_id).label("votes"))
        .join(VoteModel, VoteModel.post_id == PostsModel.id, isouter=True)
        .join(CommentsModel, CommentsModel.post_id == PostsModel.id, isouter=True)
        .group_by(PostsModel.id)
        .group_by(CommentsModel.id)
        .filter(PostsModel.id == post_id)
        .first()
    )

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return post


def search(page: int, per_page: int, search: str = "") -> list:
    posts = (
        db.query(PostsModel, func.count(VoteModel.post_id).label("votes"))
        .join(VoteModel, VoteModel.post_id == PostsModel.id, isouter=True)
        .group_by(PostsModel.id)
        .filter(PostsModel.title.contains(search))
        .limit(per_page)
        .offset((page - 1) * per_page)
        .all()
    )

    if posts is None or len(posts) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No entries found with these parameters",
        )
    return posts


def create(data: Posts, user_id: int) -> Posts:
    if len(data.title) == 0 or len(data.content) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title and content fields can not be empty.",
        )

    values = data.__dict__
    posts = PostsModel(owner_id=user_id, **values)

    db.add(posts)
    db.commit()
    db.refresh(posts)

    return posts


def update(posts_id: int, values: dict, user_id: int) -> Posts | None:
    posts = db.query(PostsModel).filter(PostsModel.id == posts_id).first()

    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    if posts.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Your are not allowed to update this post",
        )

    for key, value in values:
        setattr(posts, key, value)

    db.commit()
    db.refresh(posts)

    return posts


def published(posts_id: int, user_id: int) -> bool:
    posts = db.query(PostsModel).filter(PostsModel.id == posts_id).first()

    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    if posts.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You are not allowed to publish this post",
        )

    posts.published = True
    db.commit()
    db.refresh(posts)

    return True


def unpublished(posts_id: int, user_id: int) -> bool:
    posts = db.query(PostsModel).filter(PostsModel.id == posts_id).first()

    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    if posts.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You are not allowed to unpublished this post",
        )

    posts.published = False
    db.commit()
    db.refresh(posts)

    return True


def delete(posts_id: int, user_id: int) -> bool:
    posts = db.query(PostsModel).filter(PostsModel.id == posts_id).first()

    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    if posts.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You are not allowed to delete this post",
        )

    if posts is None or posts.owner_id != user_id:
        return False

    db.delete(posts)
    db.commit()
