from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.application.posts import PostsServices
from app.domain.accounts.entities.user import UserCredentials
from app.domain.posts.entities.posts import Posts, PostsCreate, PostsUpdate
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
    search: str = "",
) -> List[Posts]:
    """
    Get all posts
    """
    try:
        posts = PostsServices.get_posts(repo, page, per_page, search)
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return post


@router.put("/{post_id}", response_model=Posts, status_code=status.HTTP_200_OK)
def update_post(
    post_id: int,
    post: PostsUpdate,
    current_user: UserCredentials = Depends(get_current_user),
) -> Posts:
    """
    Update a post
    """
    try:
        user_id = current_user.id
        post = PostsServices.update_post(repo, post_id, post, user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return post


@router.put("/{post_id}/publish", status_code=status.HTTP_200_OK)
def publish_post(
    post_id: int,
    current_user: UserCredentials = Depends(get_current_user),
) -> dict:
    """
    Published a post
    """
    try:
        user_id = current_user.id
        PostsServices.published_post(repo, post_id, user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return {"message": f"Post {post_id} published"}


@router.put("/{post_id}/unpublish", status_code=status.HTTP_200_OK)
def unpublish_post(
    post_id: int,
    current_user: UserCredentials = Depends(get_current_user),
) -> dict:
    """
    Unpublished a post
    """
    try:
        user_id = current_user.id
        PostsServices.unpublish_post(repo, post_id, user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return {"message": f"Post {post_id} unpublished"}


@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
def delete_post(
    post_id: int,
    current_user: UserCredentials = Depends(get_current_user),
) -> None:
    """
    Delete a post
    """
    user_id = current_user.id
    PostsServices.delete_post(repo, post_id, user_id)
