from fastapi.routing import APIRouter

from app.presentation.api.healthcheck.status import \
    router as healthcheck_router


def _build_router():
    router = APIRouter()
    router.include_router(healthcheck_router, prefix="/status")
    return router


router = _build_router()
