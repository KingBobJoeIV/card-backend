from typing import TypeVar
from app.exceptions.app_exception import AppException

G = TypeVar("G")


def guard(value: G, message: str = "Assertion Error"):
    if not value:
        raise AppException(message)
    return value
