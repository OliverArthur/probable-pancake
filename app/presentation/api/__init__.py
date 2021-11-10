from fastapi.applications import FastAPI

from app.presentation.api import accounts, healthcheck


def register_routers(app: FastAPI) -> None:
    """
    Register all routers.
    """
    app.include_router(accounts.router, prefix="/accounts")
    app.include_router(healthcheck.router, prefix="/healthcheck")
    return app
