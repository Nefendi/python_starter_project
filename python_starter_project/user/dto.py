from typing import Self
from uuid import UUID

from attr import frozen

from .entity import User


@frozen
class UserDTO:
    id: UUID
    name: str
    surname: str
    age: int

    @classmethod
    def of(cls, user: User) -> Self:
        return cls(
            id=user.id.as_uuid, name=user.name, surname=user.surname, age=user.age
        )
