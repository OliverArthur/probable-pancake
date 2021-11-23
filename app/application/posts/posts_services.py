from abc import ABC
from typing import List

from fastapi import HTTPException, status

from app.domain.posts.entities.posts import Posts, PostsCreate, PostsUpdate
from app.domain.posts.interfaces.posts_repo import IPostsRepo


class PostsServices(ABC):
    """
    PostsServices class
    """

    @classmethod
    def get_post(cls, posts_repo: IPostsRepo, post_id: int) -> Posts:
        """
        Get post by id
        """
        try:
            post = posts_repo.fetch(post_id)
        except (ValueError, AttributeError, TypeError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
        return post

    @classmethod
    def get_posts(
        cls,
        posts_repo: IPostsRepo,
        page: int = 1,
        per_page: int = 10,
        search: str = "",
    ) -> List[Posts]:
        """
        Get all posts
        """
        try:
            posts = posts_repo.search(page, per_page, search)
        except (ValueError, AttributeError, TypeError) as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        return posts

    @classmethod
    def create_post(
        cls,
        posts_repo: IPostsRepo,
        data: PostsCreate,
        user_id: int,
    ) -> Posts:
        """
        Create new post
        """
        try:

            new_post = posts_repo.create(data, user_id)

        except (ValueError, AttributeError, TypeError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
        return new_post

    @classmethod
    def update_post(
        cls,
        posts_repo: IPostsRepo,
        post_id: int,
        posts_update: PostsUpdate,
        user_id: int,
    ) -> Posts:
        """
        Update post
        """
        try:
            post_updated = posts_repo.update(post_id, posts_update, user_id)
        except (ValueError, AttributeError, TypeError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )

        return post_updated

    @classmethod
    def published_post(
        cls,
        posts_repo: IPostsRepo,
        post_id: int,
        user_id: int,
    ) -> Posts:
        """
        Publish post
        """
        try:
            post = posts_repo.published(post_id, user_id)
        except (ValueError, AttributeError, TypeError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )

        return post

    @classmethod
    def unpublished_post(
        cls,
        posts_repo: IPostsRepo,
        post_id: int,
        user_id: int,
    ) -> Posts:
        """
        Unpublished post
        """
        try:
            post = posts_repo.unpublished(post_id, user_id)
        except (ValueError, AttributeError, TypeError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
        return post

    @classmethod
    def delete_post(
        cls,
        posts_repo: IPostsRepo,
        post_id: int,
        user_id: int,
    ) -> bool:
        """
        Delete post
        """
        try:
            posts_repo.delete(post_id, user_id)
        except (ValueError, AttributeError, TypeError) as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )
        return True
