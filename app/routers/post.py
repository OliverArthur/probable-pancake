from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from starlette import status

from app import models
from app.database import get_db
from app.oauth2 import get_current_user
from app.schemas import Post, PostCreate, PostUpdate

router = APIRouter()


@router.get("/posts", tags=["posts"], response_model=List[Post])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = "",
):
    return (
        db.query(models.Posts)
        .filter(models.Posts.title.contains(search))
        .limit(limit)
        .offset(offset)
        .all()
    )


@router.get("/posts/latest", tags=["posts"], response_model=Post)
def get_latest_post(db: Session = Depends(get_db)):
    return db.query(models.Posts).order_by(models.Posts.id.desc()).first()


@router.get("/posts/by_me", tags=["posts"], response_model=List[Post])
def get_my_posts(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10,
    offset: int = 0,
):
    return (
        db.query(models.Posts)
        .filter(models.Posts.owner_id == current_user.id)
        .limit(limit)
        .offset(offset)
        .all()
    )


@router.post(
    "/posts",
    status_code=status.HTTP_201_CREATED,
    tags=["posts"],
    response_model=Post,
)
def create_post(
    payload: PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    try:
        post = models.Posts(owner_id=current_user.id, **payload.dict())
        db.add(post)
        db.commit()
        db.refresh(post)
    except TypeError:
        raise HTTPException(
            detail="Invalid payload",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return post


@router.get("/posts/{post_id}", tags=["posts"], response_model=Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id {post_id} not found"
        )
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["posts"])
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id {id} not found"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of this post",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/posts/{id}", status_code=status.HTTP_200_OK, tags=["posts"], response_model=Post
)
def update_post(
    id: int,
    payload: PostUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id {id} not found"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            detail="You are not the owner of this post",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    post_query.update(payload.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
