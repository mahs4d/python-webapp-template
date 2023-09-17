"""User repository base and implementations."""
from abc import (
    ABC,
    abstractmethod,
)

from sqlalchemy import (
    delete,
    exists,
    select,
    update,
)

from python_webapp.apps.user_management.domain import User
from python_webapp.apps.user_management.repositories.db_models import UserDBModel
from python_webapp.managers.sqlalchemy_manager import SQLAlchemyManager


class UserRepository(ABC):
    """Repository to access user data."""

    @abstractmethod
    async def exists_user_by_email(self, email: str) -> bool:
        """Check if user with this email exists."""

    @abstractmethod
    async def create_user(self, email: str, firstname: str, lastname: str) -> None:
        """Create user."""

    @abstractmethod
    async def get_users(self, offset: int, limit: int) -> list[User]:
        """Get list of users."""

    @abstractmethod
    async def get_user_by_id(
        self,
        user_id: str,
    ) -> User | None:
        """Get a single user by ID."""

    @abstractmethod
    async def delete_user_by_id(
        self,
        user_id: str,
    ) -> None:
        """Delete a single user by ID."""

    @abstractmethod
    async def update_user_by_id(
        self,
        user_id: str,
        firstname: str | None = None,
        lastname: str | None = None,
    ) -> None:
        """Update a single user by ID."""


class SQLAlchemyUserRepository(UserRepository):
    """User repository implementation using SQLAlchemy."""

    def __init__(
        self,
        sqlalchemy_manager: SQLAlchemyManager,
    ) -> None:
        self.sqlalchemy_manager = sqlalchemy_manager

    async def exists_user_by_email(self, email: str) -> bool:
        async with self.sqlalchemy_manager.get_async_session() as session:
            statement = exists(1).where(UserDBModel.email == email).select()
            return await session.scalar(statement)

    async def create_user(
        self,
        email: str,
        firstname: str,
        lastname: str,
    ) -> None:
        async with self.sqlalchemy_manager.get_async_session() as session:
            db_model = UserDBModel(
                email=email,
                firstname=firstname,
                lastname=lastname,
            )

            session.add(db_model)
            await session.commit()

    async def get_users(self, offset: int = 0, limit: int = 30) -> list[User]:
        async with self.sqlalchemy_manager.get_async_session() as session:
            statement = select(UserDBModel).offset(offset).limit(limit)
            db_objects = await session.scalars(statement)
            return [obj.to_domain() for obj in db_objects]

    async def get_user_by_id(self, user_id: str) -> User | None:
        async with self.sqlalchemy_manager.get_async_session() as session:
            statement = select(UserDBModel).where(UserDBModel.id == int(user_id))
            db_obj = await session.scalar(statement)

            if db_obj is None:
                return None

            return db_obj.to_domain()

    async def delete_user_by_id(self, user_id: str) -> None:
        async with self.sqlalchemy_manager.get_async_session() as session:
            statement = delete(UserDBModel).where(UserDBModel.id == int(user_id))
            await session.execute(statement)
            await session.commit()

    async def update_user_by_id(
        self,
        user_id: str,
        firstname: str | None = None,
        lastname: str | None = None,
    ) -> None:
        async with self.sqlalchemy_manager.get_async_session() as session:
            values = {}
            if firstname is not None:
                values[UserDBModel.firstname.key] = firstname

            if lastname is not None:
                values[UserDBModel.lastname.key] = lastname

            if not values:
                return

            statement = update(UserDBModel).where(UserDBModel.id == int(user_id)).values(**values)
            await session.execute(statement)
            await session.commit()
