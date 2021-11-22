from fastapi.routing import APIRouter

from app.presentation.api.vote.vote import router as vote_router


def _build_router():
    router = APIRouter()
    router.include_router(vote_router, tags=["vote"])
    return router


router = _build_router()
