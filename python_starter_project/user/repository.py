from abc import ABC, abstractmethod

from .entity import User, UserId


class UserRepository(ABC):
    @abstractmethod
    async def add(self, user: User) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: UserId) -> User:
        pass

    @abstractmethod
    async def get_all(self) -> list[User]:
        pass
