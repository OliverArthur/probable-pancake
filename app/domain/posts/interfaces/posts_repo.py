from typing import Protocol

from sqlalchemy.sql.sqltypes import Boolean

from app.domain.posts.entities.posts import Posts


class IPostsRepo(Protocol):
    async def create(self, user_id: int, data: dict) -> Posts:
        ...

    async def fetch(self, id: int) -> Posts:
        ...

    async def search(
        self,
        page: int = 1,
        per_page: int = 10,
        search: str = "",
    ) -> list[Posts]:
        ...

    async def update(self, id: int, data: dict, user_id: int) -> Posts:
        ...

    async def published(self, id: int, user_id: int) -> bool:
        ...

    async def unpublish(self, id: int, user_id: int) -> bool:
        ...
