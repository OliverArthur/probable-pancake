from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette import status

from app import models
from app.database import get_db
from app.schemas import CreateUser, UserOut
from app.utils import hash_password

router = APIRouter()


@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut,
    tags=["users"],
)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    user = db.query(models.User).filter(models.User.email == user.email).first()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email: {user.email} already exists",
        )
    hashed_password = hash_password(new_user.password)
    new_user.password = hashed_password

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get(
    "/users/{id}",
    status_code=status.HTTP_200_OK,
    response_model=UserOut,
    tags=["users"],
)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User id {id} not found"
        )
    return user
