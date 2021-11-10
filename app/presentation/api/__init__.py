from fastapi.applications import FastAPI

from app.presentation.api import accounts, healthcheck, authentication


def register_routers(app: FastAPI) -> None:
    """
    Register all routers.
    """
    app.include_router(accounts.router, prefix="/accounts")
    app.include_router(healthcheck.router, prefix="/healthcheck")
    app.include_router(authentication.router, prefix="/authentication")
    return app
