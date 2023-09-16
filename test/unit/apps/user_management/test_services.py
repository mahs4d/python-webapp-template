from typing import Annotated
from unittest.mock import AsyncMock

import pytest

from python_webapp.apps.user_management.domain import Profile, User
from python_webapp.apps.user_management.errors import DuplicateEmailError, UserNotFoundError
from python_webapp.apps.user_management.repositories.user_repository import UserRepository
from python_webapp.apps.user_management.services import UserManagementServices


@pytest.fixture(name="user_repository_mock")
def fixture_user_repository_mock() -> Annotated[AsyncMock, UserRepository]:
    return AsyncMock(UserRepository)


@pytest.mark.asyncio()
async def test_create_user(user_repository_mock: UserRepository) -> None:
    user_repository_mock.exists_user_by_email = AsyncMock(return_value=False)
    user_repository_mock.create_user = AsyncMock()

    user_services = UserManagementServices(
        user_repository=user_repository_mock,
    )

    await user_services.create_user(
        email="foo@bar.com",
        firstname="foo",
        lastname="bar",
    )

    user_repository_mock.create_user.assert_called_once_with(
        email="foo@bar.com",
        firstname="foo",
        lastname="bar",
    )


@pytest.mark.asyncio()
async def test_create_user_duplicate_email_error(user_repository_mock: UserRepository) -> None:
    user_repository_mock.exists_user_by_email = AsyncMock(return_value=True)
    user_repository_mock.create_user = AsyncMock()

    user_services = UserManagementServices(
        user_repository=user_repository_mock,
    )

    with pytest.raises(DuplicateEmailError):
        await user_services.create_user(
            email="foo@bar.com",
            firstname="foo",
            lastname="bar",
        )

    user_repository_mock.create_user.assert_not_called()


@pytest.mark.asyncio()
async def test_get_users(user_repository_mock: UserRepository) -> None:
    users = [
        User(id="1", email="foo1@bar.com", profile=Profile()),
        User(id="2", email="foo2@bar.com", profile=Profile()),
    ]
    user_repository_mock.get_users = AsyncMock(return_value=users)

    user_services = UserManagementServices(
        user_repository=user_repository_mock,
    )

    output = await user_services.get_users(page=3)

    assert output == users
    user_repository_mock.get_users.assert_called_once_with(
        offset=40,
        limit=20,
    )


@pytest.mark.asyncio()
async def test_get_user_by_id(user_repository_mock: UserRepository) -> None:
    user = User(id="1", email="foo1@bar.com", profile=Profile())
    user_repository_mock.get_user_by_id = AsyncMock(return_value=user)

    user_services = UserManagementServices(
        user_repository=user_repository_mock,
    )

    output = await user_services.get_user_by_id(user_id="1")

    assert output == user
    user_repository_mock.get_user_by_id.assert_called_once_with(user_id="1")


@pytest.mark.asyncio()
async def test_get_user_by_id_not_found_error(user_repository_mock: UserRepository) -> None:
    user_repository_mock.get_user_by_id = AsyncMock(return_value=None)

    user_services = UserManagementServices(
        user_repository=user_repository_mock,
    )

    with pytest.raises(UserNotFoundError):
        await user_services.get_user_by_id(user_id="1")


@pytest.mark.asyncio()
async def test_delete_user_by_id(user_repository_mock: UserRepository) -> None:
    user_repository_mock.delete_user_by_id = AsyncMock()

    user_services = UserManagementServices(
        user_repository=user_repository_mock,
    )

    await user_services.delete_user_by_id(user_id="1")

    user_repository_mock.delete_user_by_id.assert_called_once_with(user_id="1")


@pytest.mark.asyncio()
async def test_update_user_by_id(user_repository_mock: UserRepository) -> None:
    user_repository_mock.update_user_by_id = AsyncMock()

    user_services = UserManagementServices(
        user_repository=user_repository_mock,
    )

    await user_services.update_user_by_id(user_id="1", firstname="foo", lastname="bar")

    user_repository_mock.update_user_by_id.assert_called_once_with(
        user_id="1",
        firstname="foo",
        lastname="bar",
    )
