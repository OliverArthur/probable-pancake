from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.application.posts import PostsServices
from app.domain.accounts.entities.user import UserCredentials
from app.domain.posts.entities.posts import Posts, PostsCreate
from app.presentation.api.authentication.auth import get_current_user
from app.presentation.container import get_dependencies

repo = get_dependencies().posts_repo
router = APIRouter(default_response_class=JSONResponse)


@router.get("/{post_id}", response_model=Posts, status_code=status.HTTP_200_OK)
def get_post(post_id: int):
    post = PostsServices.get_post(repo, post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


@router.get("/", response_model=List[Posts], status_code=status.HTTP_200_OK)
def get_posts(
    page: int = 1,
    per_page: int = 10,
) -> List[Posts]:
    """
    Get all posts
    """
    try:
        posts = PostsServices.get_posts(repo)
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return posts


@router.post("/", response_model=Posts, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostsCreate,
    current_user: UserCredentials = Depends(get_current_user),
) -> Posts:
    """
    Create a new post
    """
    try:
        user_id = current_user.id
        post = PostsServices.create_post(repo, post, user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return post
