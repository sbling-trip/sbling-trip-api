from typing import TypeVar, Generic

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int
    message: str | None
    result: T | None

    @classmethod
    def success(cls, result: T | None = None):
        return cls(code=0, message=None, result=result)

    @classmethod
    def error(cls, exception: Exception):
        return cls(code=1, message=str(exception), result=None)
