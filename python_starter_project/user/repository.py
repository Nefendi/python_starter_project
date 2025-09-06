from abc import ABC, abstractmethod

from .entity import User, UserId


class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> None:
        pass

    @abstractmethod
    def get_by_id(self, user_id: UserId) -> User:
        pass

    @abstractmethod
    def get_all(self) -> list[User]:
        pass
