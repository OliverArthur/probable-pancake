from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from toolz import pipe

from app.infrastructure.framework.config import Config
from app.presentation.api import register_routers as register_api_routers


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
    config = Config()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=[""],
    )
    return app


def init_app(config: Config) -> FastAPI:
    app: FastAPI = pipe(
        config,
        create_app,
        register_middlewares,
        register_api_routers,
    )
    return app
