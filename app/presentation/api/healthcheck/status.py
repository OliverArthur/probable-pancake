from enum import Enum

from fastapi import status
from fastapi.routing import APIRouter
from pydantic import BaseModel, Field

from app.infrastructure.framework.config import get_settings

router = APIRouter()


class StatusEmum(str, Enum):
    OK = "OK"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"


class HealthCheck(BaseModel):
    title: str = Field(..., description="Blog site API status")
    description: str = Field(..., description="Heath check for the Blog API")
    version: str = Field(..., description="Version 1.0.0")
    status: StatusEmum = Field(..., description="API current status")


@router.get(
    "/",
    response_model=HealthCheck,
    status_code=status.HTTP_200_OK,
    tags=["Health Check"],
    summary="Performs health check",
    description="Performs health check for the API and returns informantion about the running services.",
)
def health_check():
    settings = get_settings()
    return HealthCheck(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        status=StatusEmum.OK,
    )
