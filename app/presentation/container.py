from dataclasses import dataclass
from typing import Callable, cast

from app.domain.accounts.interfaces import IUserRepo
from app.domain.posts.interfaces import IPostsRepo
from app.domain.vote.interfaces import IVoteRepo
from app.infrastructure.database.repositories import (posts_repository,
                                                      user_repository,
                                                      vote_repository)


@dataclass(frozen=True)
class Dependencies:
    user_repo: IUserRepo
    posts_repo: IPostsRepo
    vote_repo: IVoteRepo


def _build_dependencies() -> Callable[[], Dependencies]:
    deps: Dependencies = Dependencies(
        user_repo=cast(IUserRepo, user_repository),
        posts_repo=cast(IPostsRepo, posts_repository),
        vote_repo=cast(IVoteRepo, vote_repository),
    )

    def fn() -> Dependencies:
        return deps

    return fn


get_dependencies = _build_dependencies()
