from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    code: str
    message: str
