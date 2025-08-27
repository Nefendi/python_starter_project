from attrs import define

from .dto import UserDTO
from .entity import User, UserId
from .repository import UserRepositoryInterface


@define
class UserFacade:
    _repository: UserRepositoryInterface

    def add(self, name: str, surname: str) -> UserDTO:
        user = User(id=UserId.new_one(), name=name, surname=surname)

        self._repository.add(user)

        return UserDTO.of(user)

    def get_by_id(self, id: UserId) -> UserDTO:
        return UserDTO.of(self._repository.get_by_id(id=id))

    def get_all(self) -> list[UserDTO]:
        return [UserDTO.of(user) for user in self._repository.get_all()]
