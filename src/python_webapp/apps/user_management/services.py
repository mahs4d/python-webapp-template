"""User management services."""

import logging
from typing import (
    Final,
)

from pydantic import (
    EmailStr,
)

from python_webapp.apps.user_management.domain import User
from python_webapp.apps.user_management.errors import (
    DuplicateEmailError,
    UserNotFoundError,
)
from python_webapp.apps.user_management.repositories.user_repository import (
    UserRepository,
)

logger = logging.getLogger(__name__)


class UserManagementServices:
    """User management application services."""

    PAGE_SIZE: Final[int] = 20

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self.user_repository = user_repository

    async def create_user(
        self,
        email: EmailStr,
        firstname: str,
        lastname: str,
    ) -> None:
        """Create a new user."""
        # Check if user with the same email already exists.
        email_exists = await self.user_repository.exists_user_by_email(
            email=email,
        )
        if email_exists:
            raise DuplicateEmailError(f"User with email `{email}` already exists!")

        # Create the user using repository.
        await self.user_repository.create_user(
            email=email,
            firstname=firstname,
            lastname=lastname,
        )

    async def get_users(self, page: int) -> list[User]:
        """Get list of users."""
        offset = (page - 1) * self.PAGE_SIZE
        return await self.user_repository.get_users(
            offset=offset,
            limit=self.PAGE_SIZE,
        )

    async def get_user_by_id(self, user_id: str) -> User:
        """Get a single user by ID."""
        user = await self.user_repository.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundError(f"User with ID `{user_id}`not found!")

        return user

    async def delete_user_by_id(self, user_id: str) -> None:
        """Delete a single user by ID."""
        await self.user_repository.delete_user_by_id(user_id=user_id)

    async def update_user_by_id(
        self,
        user_id: str,
        firstname: str | None,
        lastname: str | None,
    ) -> None:
        """Update a single user by ID."""
        await self.user_repository.update_user_by_id(
            user_id=user_id,
            firstname=firstname,
            lastname=lastname,
        )
