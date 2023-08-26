from fastapi import Request

from python_webapp_template.apps.warehouse_layout.services import WarehouseLayoutServices


def warehouse_layout_services(request: Request) -> WarehouseLayoutServices:
    return request.app.state.root_container.warehouse_layout_services()
