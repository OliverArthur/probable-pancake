from app.domain.posts.entities.posts import Posts
from app.infra.database.models.posts import Posts as PostsModel
from app.infra.database.sqlalchemy import db


def fetch(id: int) -> Posts:
    return db.query(PostsModel).filter(PostsModel.id == id).first()


def fetch_all() -> list:
    return db.query(PostsModel).all()


def create(data: Posts, user_id: int) -> Posts:
    values = data.__dict__
    posts = PostsModel(owner_id=user_id, **values)

    db.add(posts)
    db.commit()
    db.refresh(posts)

    return posts
