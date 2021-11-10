from pydantic.networks import EmailStr

from app.domain.accounts.entities.user import User
from app.infra.database.models import User as UserModel
from app.infra.database.sqlalchemy import get_db as db


async def fetch(id: int) -> User:
    user_query = db.query(UserModel).where(UserModel.id == id)
    result = await user_query.first()

    return User.parse_obj(dict(result)) if result else None


async def fetch_by_email(email: str) -> User:
    user_query = db.query(UserModel).where(UserModel.email == email)
    result = await user_query.first()

    return User.parse_obj(dict(result)) if result else None


async def create(email: EmailStr, password_hash: str) -> User:
    values = {"email": email, "password_hash": password_hash}
    user = UserModel(**values)

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return User.parse_obj(dict(user))


async def delete_one(id: int) -> None:
    user_query = db.query(UserModel).where(UserModel.id == id)
    user = await user_query.first()

    if user:
        db.delete(user)
        await db.commit()


async def update_one(id: int, email: EmailStr, password_hash: str) -> None:
    user_query = db.query(UserModel).where(UserModel.id == id)
    user = await user_query.first()

    if user:
        user.email = email
        user.password_hash = password_hash

        db.add(user)
        await db.commit()
