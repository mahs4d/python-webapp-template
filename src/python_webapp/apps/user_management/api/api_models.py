from __future__ import annotations

from pydantic import (
    BaseModel,
    EmailStr,
)

from python_webapp.apps.user_management.domain import (
    Profile,
    User,
)

# region common


class UserProfileAPIModel(BaseModel):
    """New user profile model."""

    firstname: str = ""
    lastname: str = ""

    @staticmethod
    def from_domain(profile: Profile) -> UserProfileAPIModel:
        return UserProfileAPIModel(
            firstname=profile.firstname,
            lastname=profile.lastname,
        )


class UserAPIModel(BaseModel):
    """New user model."""

    id: str
    email: EmailStr
    profile: UserProfileAPIModel

    @staticmethod
    def from_domain(user: User) -> UserAPIModel:
        return UserAPIModel(
            id=user.id,
            email=user.email,
            profile=UserProfileAPIModel.from_domain(profile=user.profile),
        )


# endregion

# region create_user


class CreateUserBody(BaseModel):
    """New user API model."""

    email: EmailStr
    profile: UserProfileAPIModel


# endregion

# region get_users


class GetUsersResponse(BaseModel):
    """Get users response model."""

    users: list[UserAPIModel]


# endregion

# region get_user_by_id


class GetUserByIDResponse(BaseModel):
    """Get user by ID response model."""

    user: UserAPIModel


# endregion

# region update_user_by_id


class UpdateUserByIDBody(BaseModel):
    """Update user by ID body model."""

    profile: UserProfileAPIModel


# endregion
