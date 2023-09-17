from pydantic import BaseModel, ConfigDict, EmailStr


class Profile(BaseModel):
    """User profile value object."""

    model_config = ConfigDict(frozen=True)

    firstname: str = ""
    lastname: str = ""


class User(BaseModel):
    """User entity."""

    id: str
    email: EmailStr
    profile: Profile
