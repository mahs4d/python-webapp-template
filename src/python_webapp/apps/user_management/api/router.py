from typing import Annotated

from fastapi import (
    Body,
    Depends,
    Query,
)
from fastapi.routing import APIRouter
from starlette import status

from python_webapp.apps.user_management.api import dependencies
from python_webapp.apps.user_management.api.api_models import (
    CreateUserBody,
    GetUserByIDResponse,
    GetUsersResponse,
    UpdateUserByIDBody,
    UserAPIModel,
)
from python_webapp.apps.user_management.services import UserManagementServices
from python_webapp.core.api.api_models import MessageResponse

router = APIRouter(
    prefix="/v1/user-management",
    tags=["user_management"],
)


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_management_services: Annotated[
        UserManagementServices,
        Depends(dependencies.user_management_services),
    ],
    body: Annotated[CreateUserBody, Body()],
) -> MessageResponse:
    await user_management_services.create_user(
        email=body.email,
        firstname=body.profile.firstname,
        lastname=body.profile.lastname,
    )

    return MessageResponse(message="ok")


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_users(
    user_management_services: Annotated[
        UserManagementServices,
        Depends(dependencies.user_management_services),
    ],
    page: Annotated[int, Query(ge=1)] = 1,
) -> GetUsersResponse:
    users = await user_management_services.get_users(page=page)

    return GetUsersResponse(users=[UserAPIModel.from_domain(user) for user in users])


@router.get("/users/{user_id:str}", status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_management_services: Annotated[
        UserManagementServices,
        Depends(dependencies.user_management_services),
    ],
    user_id: str,
) -> GetUserByIDResponse:
    user = await user_management_services.get_user_by_id(user_id=user_id)

    return GetUserByIDResponse(user=UserAPIModel.from_domain(user))


@router.delete("/users/{user_id:str}", status_code=status.HTTP_200_OK)
async def delete_user_by_id(
    user_management_services: Annotated[
        UserManagementServices,
        Depends(dependencies.user_management_services),
    ],
    user_id: str,
) -> MessageResponse:
    await user_management_services.delete_user_by_id(
        user_id=user_id,
    )

    return MessageResponse(message="ok")


@router.patch("/users/{user_id:str}", status_code=status.HTTP_200_OK)
async def update_user_by_id(
    user_management_services: Annotated[
        UserManagementServices,
        Depends(dependencies.user_management_services),
    ],
    user_id: str,
    body: Annotated[UpdateUserByIDBody, Body()],
) -> MessageResponse:
    await user_management_services.update_user_by_id(
        user_id=user_id,
        firstname=body.profile.firstname,
        lastname=body.profile.lastname,
    )

    return MessageResponse(message="ok")
