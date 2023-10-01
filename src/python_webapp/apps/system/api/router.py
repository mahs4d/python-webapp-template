from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from python_webapp.apps.system.api import dependencies
from python_webapp.apps.system.api.api_models import (
    GetHealthReportsResponse,
    GetSystemInfoResponse,
)
from python_webapp.apps.system.services import SystemServices

router = APIRouter(
    prefix="/api/v1/system",
    tags=["system"],
)


@router.get("/info", status_code=status.HTTP_200_OK)
async def get_system_info(
    system_services: Annotated[
        SystemServices,
        Depends(dependencies.system_services),
    ],
) -> GetSystemInfoResponse:
    system_info = await system_services.get_system_info()
    return GetSystemInfoResponse(system_info=system_info)


@router.get("/health_reports", status_code=status.HTTP_200_OK)
async def get_health_reports(
    system_services: Annotated[SystemServices, Depends(dependencies.system_services)],
    response: Response,
) -> GetHealthReportsResponse:
    health_reports = await system_services.get_health_reports()

    # Only return 200 if all components are healthy.
    if not all(hr.is_healthy for hr in health_reports):
        response.status_code = status.HTTP_409_CONFLICT

    return GetHealthReportsResponse(health_reports=health_reports)
