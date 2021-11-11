from dataclasses import dataclass
from typing import Callable, cast

from app.domain.accounts.interfaces import IUserRepo
from app.infra.database.repositories import user_repository


@dataclass(frozen=True)
class Dependencies:
    user_repo: IUserRepo


def _build_dependencies() -> Callable[[], Dependencies]:
    deps: Dependencies = Dependencies(user_repo=cast(IUserRepo, user_repository))

    def fn() -> Dependencies:
        return deps

    return fn


get_dependencies = _build_dependencies()
