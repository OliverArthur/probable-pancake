from typing import Callable
from dotenv import dotenv_values

from pydantic import BaseSettings, PostgresDsn

env = dotenv_values(".env")
class Config(BaseSettings):
    """
    This class is used to store the configuration of the application.
    """

    # Application settings
    APP_NAME: str = env.get("APP_NAME")
    APP_DESCRIPTION: str = env.get("APP_DESCRIPTION")
    APP_VERSION: str = "1.0.0"
    APP_OPENAPI_URL: str = "/api/v1/openapi.json"

    # Testing and development settings
    TESTING: bool = env.get("TESTING")
    DEBUG: bool = env.get("DEBUG")

    # Logging settings
    LOG_LEVEL: str = env.get("LOG_LEVEL")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Server settings.
    PORT: int = env.get("PORT")
    HOST: str = env.get("HOST")
    RELOAD: bool = env.get("RELOAD")

    # database environment variables
    DB_NAME: str = env.get("DB_NAME")
    DB_USER: str = env.get("DB_USER")
    DB_PASSWORD: str = env.get("DB_PASSWORD")
    DB_PORT: int = env.get("DB_PORT")
    DB_HOST: str = env.get("DB_HOST")
    DB_URL: PostgresDsn = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # Token settings
    JWT_SECRET_KEY: str = env.get("JWT_SECRET_KEY")

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = env.get("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    JWT_ALGORITHM: str = env.get("JWT_ALGORITHM")

    # Email settings
    MAIL_SERVER: str = env.get("MAIL_SERVER")
    MAIL_PORT: int = env.get("MAIL_PORT")
    MAIL_USE_TLS: bool = env.get("MAIL_USE_TLS")
    MAIL_USE_SSL: bool = env.get("MAIL_USE_SSL")
    MAIL_USERNAME: str = env.get("MAIL_USERNAME")
    MAIL_PASSWORD: str = env.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER: str = env.get("MAIL_DEFAULT_SENDER")


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
