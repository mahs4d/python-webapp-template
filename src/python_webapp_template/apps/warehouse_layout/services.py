import logging

from python_webapp_template.apps.warehouse_layout.domain import (
    Location,
    WarehouseLayout,
    Waypoint,
    WaypointToLocationEdge,
    WaypointToWaypointEdge,
)
from python_webapp_template.apps.warehouse_layout.repositories import WarehouseLayoutRepository

logger = logging.getLogger(__name__)


class WarehouseLayoutServices:
    def __init__(self, warehouse_layout_repository: WarehouseLayoutRepository) -> None:
        self.warehouse_layout_repository = warehouse_layout_repository

    async def upsert_warehouse_layout(
            self,
            slug: str,
            waypoints: list[Waypoint],
            locations: list[Location],
            waypoint_to_waypoint_edges: list[WaypointToWaypointEdge],
            waypoint_to_location_edges: list[WaypointToLocationEdge],
    ):
        layout = WarehouseLayout(
            slug=slug,
            waypoints=waypoints,
            locations=locations,
            waypoint_to_waypoint_edges=waypoint_to_waypoint_edges,
            waypoint_to_location_edges=waypoint_to_location_edges,
        )

        await self.warehouse_layout_repository.upsert_warehouse_layout(
            warehouse_layout=layout,
        )

    async def get_warehouse_layout_by_slug(self, slug: str) -> WarehouseLayout:
        return await self.warehouse_layout_repository.get_warehouse_layout_by_slug(slug=slug)
