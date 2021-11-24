from fastapi.routing import APIRouter

from app.presentation.api.comments.comments import router as comments_router


def _build_router():
    router = APIRouter()
    router.include_router(comments_router, tags=["comments"])
    return router


router = _build_router()
