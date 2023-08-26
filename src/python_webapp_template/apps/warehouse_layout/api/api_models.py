from pydantic import BaseModel

from python_webapp_template.apps.warehouse_layout.domain import Waypoint, Location, \
    WaypointToWaypointEdge, WaypointToLocationEdge
from pydantic import BaseModel

from python_webapp_template.apps.warehouse_layout.domain import Waypoint, Location, \
    WaypointToWaypointEdge, WaypointToLocationEdge


# region common


class LayoutAPIModel(BaseModel):
    pass


# endregion


# region get_layout_by_id


class GetLayoutByIDResponse(BaseModel):
    layout: LayoutAPIModel


# endregion


# region create_layout


class UpsertLayoutBody(BaseModel):
    waypoints: list[Waypoint]
    locations: list[Location]
    waypoint_to_waypoint_edges: list[WaypointToWaypointEdge]
    waypoint_to_location_edges: list[WaypointToLocationEdge]

# endregion
