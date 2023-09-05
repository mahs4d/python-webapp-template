from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from python_webapp.apps.user_management.domain import (
    Profile,
    User,
)
from python_webapp.core.db import Base


class UserDBModel(Base):
    """User database ORM model."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    email: Mapped[str] = mapped_column(String(), unique=True, nullable=False)

    firstname: Mapped[str] = mapped_column(String(), nullable=True, default=None)
    lastname: Mapped[str] = mapped_column(String(), nullable=True, default=None)

    def __repr__(self) -> str:
        return self.email

    def to_domain(self) -> User:
        return User(
            id=str(self.id),
            email=self.email,
            profile=Profile(
                firstname=self.firstname,
                lastname=self.lastname,
            ),
        )
