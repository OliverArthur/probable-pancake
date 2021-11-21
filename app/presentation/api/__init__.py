from fastapi.applications import FastAPI

from app.presentation.api import accounts, authentication, healthcheck, posts


def register_routers(app: FastAPI) -> None:
    """
    Register all routers.
    """
    app.include_router(accounts.router, prefix="/api/v1/accounts")
    app.include_router(healthcheck.router, prefix="/api/v1/healthcheck")
    app.include_router(authentication.router, prefix="/api/v1/authentication")
    app.include_router(posts.router, prefix="/api/v1/posts")
    return app
