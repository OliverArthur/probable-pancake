from typing import Callable

from pydantic import BaseSettings, PostgresDsn


class Config(BaseSettings):
    """
    This class is used to store the configuration of the application.
    """

    # Application settings
    APP_NAME: str = "App"
    APP_DESCRIPTION: str = "App description"
    APP_VERSION: str = "1.0.0"
    APP_OPENAPI_URL: str = "/api/v1/openapi.json"

    # Testing and development settings
    TESTING: bool = False
    DEBUG: bool = True

    # Logging settings
    LOG_LEVEL: str = "info"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Server settings.
    PORT: int = 8080
    HOST: str = "127.0.0.1"
    RELOAD: bool = True

    # database environment variables
    DB_NAME: str = "blogoliverarthur"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_PORT: int = 5432
    DB_HOST: str = "localhost"
    DB_URL: PostgresDsn = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # Token settings
    JWT_SECRET_KEY: str = (
        "841b88a5cbb69c5b03a39da7abb398aedc3a5b6841d4f025bec8e570e882d7c0"
    )

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_ALGORITHM: str = "HS256"

    # Email settings
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 465
    MAIL_USE_TLS: bool = False
    MAIL_USE_SSL: bool = True
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_DEFAULT_SENDER: str = ""


def _configure_initial_settings() -> Callable[[], Config]:
    """
    This function is used to configure the initial settings of the application.
    """

    # Configure the application settings
    settings = Config()

    def fn() -> Config:
        return settings

    return fn


get_settings = _configure_initial_settings()
