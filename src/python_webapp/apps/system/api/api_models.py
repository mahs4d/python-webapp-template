from pydantic import BaseModel

from python_webapp.apps.system.domain import SystemInfo
from python_webapp.core.health import HealthReport


# region get_system_info


class GetSystemInfoResponse(BaseModel):
    system_info: SystemInfo


# endregion

# region get_health_reports


class GetHealthReportsResponse(BaseModel):
    health_reports: list[HealthReport]


# endregion
