from abc import ABC, abstractmethod

from pydantic import BaseModel


class HealthReport(BaseModel):
    component: str
    is_healthy: bool


class HealthReportable(ABC):
    @abstractmethod
    async def get_health_report(self) -> HealthReport:
        pass
