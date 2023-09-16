from unittest.mock import AsyncMock

import pytest

from python_webapp.apps.system.domain import SystemInfo
from python_webapp.apps.system.services import SystemServices
from python_webapp.config import Config
from python_webapp.core.health import HealthReport, HealthReportable


@pytest.mark.asyncio
async def test_get_system_info():
    system_name_mock = "foo"
    system_version_mock = "1.2.3"

    config = AsyncMock(Config)
    config.system_name = system_name_mock
    config.system_version = system_version_mock

    expected_output = SystemInfo(
        name=system_name_mock,
        version=system_version_mock,
    )

    system_services = SystemServices(
        config=config,
        health_reportables=[],
    )
    output = await system_services.get_system_info()

    assert output == expected_output


@pytest.mark.asyncio
async def test_get_health_reports():
    health_report1_mock = HealthReport(
        component="component1",
        is_healthy=True,
    )
    health_report2_mock = HealthReport(
        component="component2",
        is_healthy=False,
    )

    health_reportable1 = AsyncMock(HealthReportable)
    health_reportable1.get_health_report = AsyncMock(return_value=health_report1_mock)
    health_reportable2 = AsyncMock(HealthReportable)
    health_reportable2.get_health_report = AsyncMock(return_value=health_report2_mock)

    expected_output = [
        health_report1_mock,
        health_report2_mock,
    ]

    system_services = SystemServices(
        config=AsyncMock(Config),
        health_reportables=[
            health_reportable1,
            health_reportable2,
        ],
    )
    output = await system_services.get_health_reports()

    assert output == expected_output
