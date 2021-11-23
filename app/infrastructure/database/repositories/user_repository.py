from pydantic.networks import EmailStr

from app.domain.accounts.entities.user import User
from app.infrastructure.database.models.user import User as UserModel
from app.infrastructure.database.sqlalchemy import db


def fetch(id: int) -> User:
    return db.query(UserModel).where(UserModel.id == id).first()


def fetch_by_email(email: str) -> User:
    return db.query(UserModel).where(UserModel.email == email).first()


def create(email: EmailStr, password_hash: str) -> User:
    values = {"email": email, "password": password_hash}
    user = UserModel(**values)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_me(user: User, values: dict) -> User:
    for k, v in values:
        setattr(user, k, v)

    db.commit()
    db.refresh(user)

    return user