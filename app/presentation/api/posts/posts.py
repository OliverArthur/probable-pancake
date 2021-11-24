from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.application.posts import PostsServices
from app.domain.accounts.entities.user import UserCredentials
from app.domain.posts.entities.posts import (
    Posts,
    PostsCreate,
    PostsInDBOut,
    PostsUpdate,
)
from app.presentation.api.authentication.auth import get_current_user
from app.presentation.container import get_dependencies

repo = get_dependencies().posts_repo
router = APIRouter(default_response_class=JSONResponse)


@router.get(
    "/{post_id}",
    response_model=PostsInDBOut,
    status_code=status.HTTP_200_OK,
)
def get_post(post_id: int):
    """get a single post by id

    :param post_id: id of the post
    :return: Posts entity
    """
    return PostsServices.get_post(repo, post_id)


@router.get(
    "/",
    response_model=List[PostsInDBOut],
    status_code=status.HTTP_200_OK,
)
def get_posts(
    page: int = 1,
    per_page: int = 10,
    search: str = "",
) -> List[Posts]:
    """Get a list of posts

    :param page: initial page to show for the pagination
    :param per_page: the number of posts to show per page
    :param search: the terms to search a posts.
    :return: List[Posts]
    """
    return PostsServices.get_posts(repo, page, per_page, search)


@router.post("/", response_model=Posts, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostsCreate,
    current_user: UserCredentials = Depends(get_current_user),
) -> Posts:
    """Create a new post

    :param post: payload to create the post, title and content are required fields
    :param current_user: the owner of the posts
    :return: Post entity
    """
    user_id = current_user.id
    post = PostsServices.create_post(repo, post, user_id)
    return post


@router.put("/{post_id}", response_model=Posts, status_code=status.HTTP_200_OK)
def update_post(
    post_id: int,
    post: PostsUpdate,
    current_user: UserCredentials = Depends(get_current_user),
) -> Posts:
    """Update a posts

    :param post_id: the post id to be updated
    :param post: the new post data.
    :param current_user: the owner of the post
    :return: Post entity
    """
    user_id = current_user.id
    post = PostsServices.update_post(repo, post_id, post, user_id)
    return post


@router.put("/{post_id}/publish", status_code=status.HTTP_200_OK)
def publish_post(
    post_id: int,
    current_user: UserCredentials = Depends(get_current_user),
) -> dict:
    """Published a post

    :param post_id: the post id to be published
    :param current_user: the owner of the post
    :return: dict
    """
    user_id = current_user.id
    PostsServices.published_post(repo, post_id, user_id)
    return {"message": f"Post {post_id} published"}


@router.put("/{post_id}/unpublished", status_code=status.HTTP_200_OK)
def unpublished_post(
    post_id: int,
    current_user: UserCredentials = Depends(get_current_user),
) -> dict:
    """Unpublished a post

    :param post_id: the post id to be unpublished
    :param current_user: the owner of the post
    :return: dict
    """
    user_id = current_user.id
    PostsServices.unpublished_post(repo, post_id, user_id)
    return {"message": f"Post {post_id} unpublished"}


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    current_user: UserCredentials = Depends(get_current_user),
) -> None:
    """Delete a post

    :param post_id: the post id to be deleted
    :param current_user: the owner of the post
    :return: None
    """
    user_id = current_user.id
    PostsServices.delete_post(repo, post_id, user_id)
