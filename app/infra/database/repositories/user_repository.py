from pydantic.networks import EmailStr

from app.domain.accounts.entities.user import User
from app.infra.database.models import User as UserModel
from app.infra.database.sqlalchemy import session as db


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


def delete_one(id: int) -> None:
    user_query = db.query(UserModel).where(UserModel.id == id)
    user = user_query.first()

    if user:
        db.delete(user)
        db.commit()


def update_one(id: int, email: EmailStr, password_hash: str) -> None:
    user_query = db.query(UserModel).where(UserModel.id == id)
    user = user_query.first()

    if user:
        user.email = email
        user.password_hash = password_hash

        db.add(user)
        db.commit()
