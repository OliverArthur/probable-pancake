from fastapi.applications import FastAPI

from app.presentation.api import accounts, authentication, healthcheck


def register_routers(app: FastAPI) -> None:
    """
    Register all routers.
    """
    app.include_router(accounts.router, prefix="/api/v1/accounts")
    app.include_router(healthcheck.router, prefix="/api/v1/healthcheck")
    app.include_router(authentication.router, prefix="/api/v1/authentication")
    return app
