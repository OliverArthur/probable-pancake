from typing import Protocol

from app.domain.posts.entities.posts import Posts, PostsUpdate, PostsCreate


class IPostsRepo(Protocol):
    async def create(self, user_id: int, data: PostsCreate) -> Posts:
        ...

    async def fetch(self, post_id: int) -> Posts:
        ...

    async def search(
        self,
        page: int = 1,
        per_page: int = 10,
        search: str = "",
    ) -> list[Posts]:
        ...

    async def update(self, post_id: int, data: PostsUpdate, user_id: int) -> Posts:
        ...

    async def published(self, post_id: int, user_id: int) -> bool:
        ...

    async def unpublished(self, post_id: int, user_id: int) -> bool:
        ...

    async def delete(self, post_id: int, user_id: int) -> None:
        ...
