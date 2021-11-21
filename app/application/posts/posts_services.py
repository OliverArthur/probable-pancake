from abc import ABC
from typing import List

from fastapi import HTTPException, status

from app.domain.posts.entities.posts import Posts, PostsCreate
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
    def get_posts(cls, posts_repo: IPostsRepo) -> List[Posts]:
        """
        Get all posts
        """
        posts = posts_repo.fetch_all()

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
