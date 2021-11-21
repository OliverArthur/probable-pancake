from typing import Protocol

from app.domain.posts.entities.posts import Posts


class IPostsRepo(Protocol):
    async def create(self, user_id: int, data: dict) -> Posts:
        ...

    async def fetch(self, id: int) -> Posts:
        ...

    async def fetch_all(self, page: int = 1, per_page: int = 10) -> list[Posts]:
        ...
