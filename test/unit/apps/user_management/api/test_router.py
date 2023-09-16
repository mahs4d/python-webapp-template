from typing import Annotated
from unittest.mock import AsyncMock

import pytest

from python_webapp.apps.user_management.api.api_models import CreateUserBody, UserProfileAPIModel
from python_webapp.apps.user_management.api.router import create_user
from python_webapp.apps.user_management.services import UserManagementServices
from python_webapp.core.api.api_models import MessageResponse


@pytest.fixture(name='user_management_services_mock')
def fixture_user_management_services_mock() -> Annotated[AsyncMock, UserManagementServices]:
    return AsyncMock(UserManagementServices)


@pytest.mark.asyncio
async def test_create_user(user_management_services_mock: UserManagementServices):
    user_management_services_mock.create_user = AsyncMock()

    output = await create_user(
        user_management_services=user_management_services_mock,
        body=CreateUserBody(
            email='foo@bar.com',
            profile=UserProfileAPIModel(
                firstname='foo',
                lastname='bar',
            )
        ),
    )

    assert output == MessageResponse(
        message='ok',
    )
    user_management_services_mock.create_user.assert_called_once_with(
        email='foo@bar.com',
        firstname='foo',
        lastname='bar',
    )
