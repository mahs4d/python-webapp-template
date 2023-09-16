from typing import Annotated
from unittest.mock import AsyncMock

import pytest
from fastapi import Response
from starlette import status

from python_webapp.apps.system.api.api_models import GetHealthReportsResponse, GetSystemInfoResponse
from python_webapp.apps.system.api.router import get_health_reports, get_system_info
from python_webapp.apps.system.domain import SystemInfo
from python_webapp.apps.system.services import SystemServices
from python_webapp.core.health import HealthReport


@pytest.fixture(name="response_mock")
def fixture_response_mock() -> Annotated[AsyncMock, Response]:
    response_mock = AsyncMock(Response)
    response_mock.status_code = status.HTTP_200_OK

    return response_mock


@pytest.fixture(name="system_services_mock")
def fixture_system_services_mock() -> Annotated[AsyncMock, SystemServices]:
    return AsyncMock(SystemServices)


@pytest.mark.asyncio()
async def test_get_system_info(system_services_mock: SystemServices) -> None:
    system_info = SystemInfo(
        name="foo",
        version="1.2.3",
    )
    system_services_mock.get_system_info = AsyncMock(
        return_value=system_info,
    )

    output = await get_system_info(
        system_services=system_services_mock,
    )

    assert output == GetSystemInfoResponse(
        system_info=system_info,
    )


@pytest.mark.asyncio()
async def test_get_health_reports(
    response_mock: Response,
    system_services_mock: SystemServices,
) -> None:
    health_reports = [
        HealthReport(
            component="api",
            is_healthy=True,
        ),
        HealthReport(
            component="db",
            is_healthy=True,
        ),
    ]
    system_services_mock.get_health_reports = AsyncMock(
        return_value=health_reports,
    )

    output = await get_health_reports(
        system_services=system_services_mock,
        response=response_mock,
    )

    assert output == GetHealthReportsResponse(
        health_reports=health_reports,
    )
    assert response_mock.status_code == status.HTTP_200_OK


@pytest.mark.asyncio()
async def test_get_health_reports_unhealthy(
    response_mock: Response,
    system_services_mock: SystemServices,
) -> None:
    health_reports = [
        HealthReport(
            component="api",
            is_healthy=True,
        ),
        HealthReport(
            component="event",
            is_healthy=False,
        ),
        HealthReport(
            component="db",
            is_healthy=True,
        ),
    ]
    system_services_mock.get_health_reports = AsyncMock(
        return_value=health_reports,
    )

    output = await get_health_reports(
        system_services=system_services_mock,
        response=response_mock,
    )

    assert output == GetHealthReportsResponse(
        health_reports=health_reports,
    )
    assert response_mock.status_code == status.HTTP_409_CONFLICT
