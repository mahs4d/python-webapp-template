from python_webapp.apps.system.domain import SystemInfo
from python_webapp.config import Config
from python_webapp.core.health import HealthReport, HealthReportable


class SystemServices:
    def __init__(
        self,
        config: Config,
        health_reportables: list[HealthReportable],
    ) -> None:
        self.config = config
        self.health_reportables = health_reportables

    async def get_system_info(self) -> SystemInfo:
        """Get general system information."""
        return SystemInfo(
            name=self.config.system_name,
            version=self.config.system_version,
        )

    async def get_health_reports(self) -> list[HealthReport]:
        """Get list of health reports gathered from different components of the system."""
        health_reports = []
        for health_reportable in self.health_reportables:
            health_report = await health_reportable.get_health_report()
            health_reports.append(health_report)

        return health_reports
