from __future__ import annotations

from typing import cast, override
from uuid import UUID, uuid4

from attr import frozen
from attrs import define


@frozen
class UserId:
    _id: UUID

    @property
    def as_uuid(self) -> UUID:
        return self._id

    @staticmethod
    def new_one() -> UserId:
        return UserId(uuid4())


@define
class User:
    id: UserId
    name: str
    surname: str

    @override
    def __eq__(self, other: object) -> bool:
        return self.id == cast(User, other).id
