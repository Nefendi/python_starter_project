from attrs import define

from ..database import transactional
from .dto import UserDTO
from .entity import User, UserId
from .repository import UserRepository


@define
class UserFacade:
    _repository: UserRepository

    @transactional
    def add(self, name: str, surname: str) -> UserDTO:
        user = User(name=name, surname=surname)

        self._repository.add(user)

        return UserDTO.of(user)

    @transactional
    def update(self, user_id: UserId, name: str, surname: str) -> UserDTO:
        user = self._repository.get_by_id(user_id)

        user.name = name
        user.surname = surname

        self._repository.update(user)

        return UserDTO.of(user)

    @transactional
    def get_by_id(self, user_id: UserId) -> UserDTO:
        return UserDTO.of(self._repository.get_by_id(user_id=user_id))

    @transactional
    def get_all(self) -> list[UserDTO]:
        return [UserDTO.of(user) for user in self._repository.get_all()]
