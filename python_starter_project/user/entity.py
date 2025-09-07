from __future__ import annotations

from datetime import date
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
    date_of_birth: date
    _id: UserId = UserId.new_one()

    @property
    def id(self) -> UserId:
        return self._id

    @property
    def age(self) -> int:
        today = date.today()
        born = self.date_of_birth

        return (
            today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        )

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False

        return self.id == other.id
