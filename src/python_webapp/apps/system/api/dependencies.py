from fastapi import Request

from python_webapp.apps.system.services import SystemServices


async def system_services(request: Request) -> SystemServices:
    return request.app.state.root_container.system_services()
