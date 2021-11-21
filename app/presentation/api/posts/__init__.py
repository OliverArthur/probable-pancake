from fastapi.routing import APIRouter

from app.presentation.api.posts.posts import router as posts_router


def _build_router():
    router = APIRouter()
    router.include_router(posts_router, tags=["posts"])
    return router


router = _build_router()
