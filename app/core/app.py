from fastapi import FastAPI
from toolz import pipe

from app.core.config import Config
from app.infra.database.sqlalchemy import Base
from app.infra.database.sqlalchemy import engine
from app.presentation.api import register_routers as register_api_routers

Base.metadata.create_all(bind=engine)


def create_app(config: Config) -> FastAPI:
    return FastAPI(
        title=config.APP_NAME,
        description=config.APP_DESCRIPTION,
        version=config.APP_VERSION,
        openapi_url=config.APP_OPENAPI_URL,
        docs_url="/docs",
        redoc_url="/redoc",
        debug=config.DEBUG,
    )


def register_middlewares(app: FastAPI) -> FastAPI:
    return app


def init_app(config: Config) -> FastAPI:
    app: FastAPI = pipe(
        config,
        create_app,
        register_middlewares,
        register_api_routers,
    )
    return app
