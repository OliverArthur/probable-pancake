from fastapi import HTTPException, status
from pydantic.networks import EmailStr

from app.domain.accounts.entities.user import User
from app.infrastructure.database.models.user import User as UserModel
from app.infrastructure.database.sqlalchemy import db


def fetch(user_id: int) -> User:
    account = db.query(UserModel).where(UserModel.id == user_id).first()

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    return account


def fetch_by_email(email: str) -> User:
    account = db.query(UserModel).where(UserModel.email == email).first()

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    return account


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
