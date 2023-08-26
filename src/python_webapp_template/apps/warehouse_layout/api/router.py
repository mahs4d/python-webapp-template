from typing import Annotated

from fastapi import APIRouter, Depends, Body
from starlette import status

from python_webapp_template.apps.warehouse_layout.api import dependencies
from python_webapp_template.apps.warehouse_layout.api.api_models import (
    GetLayoutByIDResponse,
    UpsertLayoutBody,
)
from python_webapp_template.apps.warehouse_layout.services import WarehouseLayoutServices
from python_webapp_template.core.api.api_models import MessageResponse

router = APIRouter(
    prefix="/api/v1/warehouse_layout",
    tags=["warehouse_layout"],
)


@router.put("/layouts/{slug:str}", status_code=status.HTTP_201_CREATED)
async def upsert_layout(
        warehouse_layout_services: Annotated[
            WarehouseLayoutServices,
            Depends(dependencies.warehouse_layout_services),
        ],
        slug: str,
        body: Annotated[UpsertLayoutBody, Body],
) -> MessageResponse:
    await warehouse_layout_services.upsert_warehouse_layout(
        slug=slug,
        waypoints=body.waypoints,
        locations=body.locations,
        waypoint_to_waypoint_edges=body.waypoint_to_waypoint_edges,
        waypoint_to_location_edges=body.waypoint_to_location_edges,
    )

    return MessageResponse(message="ok")


@router.get("/layouts/{slug:str}", status_code=status.HTTP_200_OK)
async def get_layout_by_slug(
        warehouse_layout_services: Annotated[
            WarehouseLayoutServices,
            Depends(dependencies.warehouse_layout_services),
        ],
        slug: str,
) -> GetLayoutByIDResponse:
    pass
