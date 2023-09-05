from fastapi.requests import Request

from python_webapp.apps.user_management.services import UserManagementServices


async def user_management_services(request: Request) -> UserManagementServices:
    return request.app.state.root_container.user_management_services()
