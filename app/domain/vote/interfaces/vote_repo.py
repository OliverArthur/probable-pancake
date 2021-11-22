from typing import Protocol

from app.domain.vote.entities.vote import Vote


class IVoteRepo(Protocol):
    async def fetch(self, post_id: int) -> Vote:
        ...

    async def vote(
        self,
        user_id: int,
        post_id: int,
    ) -> Vote:
        ...

    async def unvote(self, post_id: int) -> Vote:
        ...
