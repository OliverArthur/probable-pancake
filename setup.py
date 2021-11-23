from setuptools import setup
from app.infrastructure.framework.config import Config

_SETTINGS = Config()


setup(
    name=_SETTINGS.APP_NAME,
    version=_SETTINGS.APP_VERSION,
    packages=[
        "app",
        "scripts"
    ],
    url=None,
    license="",
    author="Oliver Arthur",
    author_email="development@oliverarthurnardi.com",
    description=_SETTINGS.APP_DESCRIPTION,
)