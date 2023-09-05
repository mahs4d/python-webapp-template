class AppError(Exception):
    """Base for known app errors."""

    def __init__(
        self,
        status: int,
        code: str,
        message: str,
    ) -> None:
        self.status = status
        self.code = code
        self.message = message

        super().__init__(f'{str} {code.lower()} > "{message}"')
