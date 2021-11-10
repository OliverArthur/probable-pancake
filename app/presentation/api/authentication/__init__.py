from fastapi.routing import APIRouter

from app.presentation.api.authentication.auth import router as user_auth


def _build_router():
    router = APIRouter()
    router.include_router(user_auth, tags=["Authentication"])
    return router


router = _build_router()
