from __future__ import annotations

from typing import override
from uuid import UUID, uuid4

from attrs import define, frozen


@frozen
class UserId:
    uuid: UUID

    @property
    def as_uuid(self) -> UUID:
        return self.uuid

    @staticmethod
    def new_one() -> UserId:
        return UserId(uuid4())


# INFO: slots=False is needed for SQLAlchemy's imperative mapping
@define(slots=False)
class User:
    name: str
    surname: str
    _id: UserId = UserId.new_one()

    @property
    def id(self) -> UserId:
        return self._id

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False

        return self.id == other.id
