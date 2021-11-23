from sqlalchemy.sql import func

from app.domain.posts.entities.posts import Posts
from app.infrastructure.database.models.posts import Posts as PostsModel
from app.infrastructure.database.models.vote import Vote as VoteModel
from app.infrastructure.database.sqlalchemy import db


def fetch(id: int) -> Posts:
    return (
        db.query(PostsModel, func.count(VoteModel.post_id).label("votes"))
        .join(VoteModel, VoteModel.post_id == PostsModel.id, isouter=True)
        .group_by(PostsModel.id)
        .filter(PostsModel.id == id)
        .first()
    )


def search(page: int, per_page: int, search: str = "") -> list:
    return (
        db.query(PostsModel, func.count(VoteModel.post_id).label("votes"))
        .join(VoteModel, VoteModel.post_id == PostsModel.id, isouter=True)
        .group_by(PostsModel.id)
        .filter(PostsModel.title.contains(search))
        .limit(per_page)
        .offset((page - 1) * per_page)
        .all()
    )


def create(data: Posts, user_id: int) -> Posts:

    if len(data.title) == 0 or len(data.content) == 0:
        return None

    values = data.__dict__
    posts = PostsModel(owner_id=user_id, **values)

    db.add(posts)
    db.commit()
    db.refresh(posts)

    return posts


def update(posts_id: int, values: dict, user_id: int) -> Posts:
    posts = fetch(posts_id)

    if posts is None or posts.owner_id != user_id:
        return None

    for key, value in values:
        setattr(posts, key, value)

    db.commit()
    db.refresh(posts)

    return posts


def published(posts_id: int, user_id: int) -> bool:
    posts = fetch(posts_id)

    if posts is None or posts.owner_id != user_id:
        return False

    posts.published = True
    db.commit()
    db.refresh(posts)

    return True


def unpublish(posts_id: int, user_id: int) -> bool:
    post = fetch(posts_id)

    if post is None or post.owner_id != user_id:
        return False

    post.published = False
    db.commit()
    db.refresh(post)

    return True


def delete(posts_id: int, user_id: int) -> bool:
    post = fetch(posts_id)

    if post is None or post.owner_id != user_id:
        return False

    db.delete(post)
    db.commit()
