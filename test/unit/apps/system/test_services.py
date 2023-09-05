from unittest.mock import AsyncMock

import pytest

from python_webapp.apps.system.domain import SystemInfo
from python_webapp.apps.system.services import SystemServices
from python_webapp.config import Config
from python_webapp.core.health import HealthReport, HealthReportable


@pytest.mark.asyncio
async def test_get_system_info():
    """Test `get_system_info` method."""
    mock_system_name = "foo"
    mock_system_version = "1.2.3"

    config = AsyncMock(Config)
    config.system_name = mock_system_name
    config.system_version = mock_system_version

    system_services = SystemServices(
        config=config,
        health_reportables=[],
    )

    system_info = await system_services.get_system_info()

    assert system_info == SystemInfo(
        name=mock_system_name,
        version=mock_system_version,
    )


@pytest.mark.asyncio
async def test_get_health_reports():
    """Test `get_health_reports` method."""
    mock_health_report1 = HealthReport(
        component="component1",
        is_healthy=True,
    )
    mock_health_report2 = HealthReport(
        component="component2",
        is_healthy=False,
    )

    health_reportable1 = AsyncMock(HealthReportable)
    health_reportable1.get_health_report = AsyncMock(return_value=mock_health_report1)
    health_reportable2 = AsyncMock(HealthReportable)
    health_reportable2.get_health_report = AsyncMock(return_value=mock_health_report2)

    system_services = SystemServices(
        config=AsyncMock(Config),
        health_reportables=[
            health_reportable1,
            health_reportable2,
        ],
    )

    health_reports = await system_services.get_health_reports()

    assert health_reports == [
        mock_health_report1,
        mock_health_report2,
    ]
