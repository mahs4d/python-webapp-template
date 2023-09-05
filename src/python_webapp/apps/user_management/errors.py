"""User management errors."""

from starlette import status

from python_webapp.core.errors import AppError


class DuplicateEmailError(AppError):
    """Error to raise when duplicate email address is detected."""

    def __init__(self, message: str) -> None:
        super().__init__(
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            code="user_management:duplicate_email",
            message=message,
        )


class UserNotFoundError(AppError):
    """Error to raise when user was not found."""

    def __init__(self, message: str) -> None:
        super().__init__(
            status=status.HTTP_404_NOT_FOUND,
            code="user_management:user_not_found",
            message=message,
        )
