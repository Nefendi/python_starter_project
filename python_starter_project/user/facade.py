from datetime import date

from attrs import define

from ..database import transactional
from .dto import UserDTO
from .entity import User, UserId
from .repository import UserRepository


@define
class UserFacade:
    _repository: UserRepository

    @transactional
    async def add(self, name: str, surname: str, date_of_birth: date) -> UserDTO:
        user = User(name=name, surname=surname, date_of_birth=date_of_birth)

        await self._repository.add(user)

        return UserDTO.of(user)

    @transactional
    async def update(self, user_id: UserId, name: str, surname: str) -> UserDTO:
        user = await self._repository.get_by_id(user_id)

        user.name = name
        user.surname = surname

        return UserDTO.of(user)

    @transactional
    async def get_by_id(self, user_id: UserId) -> UserDTO:
        return UserDTO.of(await self._repository.get_by_id(user_id=user_id))

    @transactional
    async def get_all(self) -> list[UserDTO]:
        return [UserDTO.of(user) for user in await self._repository.get_all()]
