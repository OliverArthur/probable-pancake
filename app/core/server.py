import uvicorn

from app.core.app import init_app
from app.core.config import get_settings

_SETTINGS = get_settings()

api_server = init_app(_SETTINGS)


def start_server():
    settings = get_settings()
    uvicorn.run(
        "app.core.server:api_server",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL,
    )
