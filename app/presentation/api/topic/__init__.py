from fastapi.routing import APIRouter

from app.presentation.api.topic.topic import router as topic_router


def _build_router():
    router = APIRouter()
    router.include_router(topic_router, tags=["topics"])
    return router


router = _build_router()