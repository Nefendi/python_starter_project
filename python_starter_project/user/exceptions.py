from python_starter_project.shared import DomainException

from .entity import UserId


class NoUserFoundException(DomainException):
    def __init__(self, id: UserId) -> None:
        message = f"User with id = '{id}' not found"

        super().__init__(message)
