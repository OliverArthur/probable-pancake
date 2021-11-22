from app.domain.posts.entities.posts import Posts
from app.infra.database.models.posts import Posts as PostsModel
from app.infra.database.sqlalchemy import db


def fetch(id: int) -> Posts:
    return db.query(PostsModel).filter(PostsModel.id == id).first()


def search(page: int, per_page: int, search: str = "") -> list:
    return (
        db.query(PostsModel)
        .filter(PostsModel.title.contains(search))
        .limit(per_page)
        .offset((page - 1) * per_page)
        .all()
    )


def create(data: Posts, user_id: int) -> Posts:
    values = data.__dict__
    posts = PostsModel(owner_id=user_id, **values)

    db.add(posts)
    db.commit()
    db.refresh(posts)

    return posts


def update(posts_id: int, values: dict, user_id: int) -> Posts:
    posts = fetch(posts_id)
    if posts.owner_id != user_id:
        return None

    for key, value in values:
        setattr(posts, key, value)

    db.commit()
    db.refresh(posts)

    return posts


def published(posts_id: int, user_id: int) -> bool:
    posts = fetch(posts_id)
    if posts.owner_id != user_id:
        return False

    posts.published = True
    db.commit()
    db.refresh(posts)

    return True


def unpublish(posts_id: int, user_id: int) -> bool:
    posts = fetch(posts_id)
    if posts.owner_id != user_id:
        return False

    posts.published = False
    db.commit()
    db.refresh(posts)

    return True


def delete(posts_id: int, user_id: int) -> bool:
    posts = fetch(posts_id)
    if posts.owner_id != user_id:
        return False

    db.delete(posts)
    db.commit()
