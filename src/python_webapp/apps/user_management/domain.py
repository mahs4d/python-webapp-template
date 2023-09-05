from typing import Self

from pydantic import BaseModel, EmailStr, ConfigDict


class Profile(BaseModel):
    """User profile value object."""

    model_config = ConfigDict(frozen=True)

    firstname: str | None = None
    lastname: str | None = None


class User(BaseModel):
    """User entity."""

    id: str
    email: EmailStr
    profile: Profile

    def __eq__(self, other: Self) -> bool:
        return self.id == other.id
