from fastapi.routing import APIRouter

from app.presentation.api.accounts.user import router as user_router


def _build_router():
    router = APIRouter()
    router.include_router(user_router, prefix="/user", tags=["User"])
    return router


router = _build_router()
