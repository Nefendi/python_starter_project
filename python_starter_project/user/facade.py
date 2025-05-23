from collections.abc import Iterator
from uuid import UUID, uuid4

from attrs import define

from .entity import User
from .repository import UserRepositoryInterface


@define
class UserFacade:
    _repository: UserRepositoryInterface

    def add(self, name: str, surname: str) -> User:
        user = User(id=uuid4(), name=name, surname=surname)

        self._repository.add(user)

        return user

    def get_by_id(self, id: UUID) -> User:
        return self._repository.get_by_id(id=id)

    def get_all(self) -> Iterator[User]:
        return self._repository.get_all()
