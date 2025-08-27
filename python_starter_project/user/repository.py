from abc import ABC, abstractmethod
from typing import override
from uuid import UUID

from sqlalchemy import select

from python_starter_project.database import ScopedSession

from .entity import User
from .exceptions import NoUserFoundException
from .model import UserModel


class UserRepositoryInterface(ABC):
    @abstractmethod
    def add(self, user: User) -> None:
        pass

    @abstractmethod
    def get_by_id(self, id: UUID) -> User:
        pass

    @abstractmethod
    def get_all(self) -> list[User]:
        pass


class UserPostgresRepository(UserRepositoryInterface):
    @override
    def add(self, user: User) -> None:
        session = ScopedSession()

        user_to_add = self._entity_to_model(user)

        session.add(user_to_add)
        session.flush([user_to_add])

    @override
    def get_by_id(self, id: UUID) -> User:
        session = ScopedSession()

        stmt = select(UserModel).where(UserModel.id == id)

        retrieved_user = session.scalar(stmt)

        if not retrieved_user:
            raise NoUserFoundException()

        return self._model_to_entity(retrieved_user)

    @override
    def get_all(self) -> list[User]:
        session = ScopedSession()

        stmt = select(UserModel)

        retrieved_users = session.scalars(stmt)

        return [self._model_to_entity(user) for user in retrieved_users]

    def _entity_to_model(self, entity: User) -> UserModel:
        return UserModel(id=entity.id, name=entity.name, surname=entity.surname)

    def _model_to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            name=model.name,
            surname=model.surname,
        )
