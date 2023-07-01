from typing import cast
from uuid import UUID

from attrs import define


@define
class User:
    id: UUID
    name: str
    surname: str

    def __eq__(self, other: object) -> bool:
        return self.id == cast(User, other).id
