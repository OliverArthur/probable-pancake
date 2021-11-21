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
        post = posts_repo.fetch(post_id)

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Posts not found",
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
        posts = posts_repo.search(page, per_page, search)

        if not posts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Posts not found",
            )

        return posts

    @classmethod
    def create_post(
        self,
        posts_repo: IPostsRepo,
        posts_create: PostsCreate,
        user_id: int,
    ) -> Posts:
        """
        Create new post
        """
        return posts_repo.create(posts_create, user_id)

    @classmethod
    def update_post(
        self,
        posts_repo: IPostsRepo,
        post_id: int,
        posts_update: PostsUpdate,
        user_id: int,
    ) -> Posts:
        """
        Update post
        """
        post = posts_repo.update(post_id, posts_update, user_id)

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Posts not found",
            )

        return post
