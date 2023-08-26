from __future__ import annotations

import uuid
from enum import StrEnum, auto

from pydantic import BaseModel, Field
from pydantic.types import UUID4


class Waypoint(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)


class TemperatureZone(StrEnum):
    AMBIENT = auto()
    CHILLED = auto()


class Location(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    barcode: str
    temperature_zone: TemperatureZone


class WaypointToWaypointEdge(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    waypoint_id: UUID4
    target_waypoint_id: UUID4


class WaypointToLocationEdge(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    waypoint_id: UUID4
    target_location_id: UUID4


class WarehouseLayout(BaseModel):
    slug: str
    waypoints: list[Waypoint]
    locations: list[Location]
    waypoint_to_waypoint_edges: list[WaypointToWaypointEdge]
    waypoint_to_location_edges: list[WaypointToLocationEdge]
