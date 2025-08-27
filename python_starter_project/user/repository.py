from abc import ABC, abstractmethod
from typing import override

from sqlalchemy import select

from python_starter_project.database import ScopedSession

from .entity import User, UserId
from .exceptions import NoUserFoundException
from .model import UserModel


class UserRepositoryInterface(ABC):
    @abstractmethod
    def add(self, user: User) -> None:
        pass

    @abstractmethod
    def get_by_id(self, id: UserId) -> User:
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
    def get_by_id(self, id: UserId) -> User:
        session = ScopedSession()

        stmt = select(UserModel).where(UserModel.id == id.as_uuid)

        retrieved_user = session.scalar(stmt)

        if not retrieved_user:
            raise NoUserFoundException(id)

        return self._model_to_entity(retrieved_user)

    @override
    def get_all(self) -> list[User]:
        session = ScopedSession()

        stmt = select(UserModel)

        retrieved_users = session.scalars(stmt)

        return [self._model_to_entity(user) for user in retrieved_users]

    def _entity_to_model(self, entity: User) -> UserModel:
        return UserModel(id=entity.id.as_uuid, name=entity.name, surname=entity.surname)

    def _model_to_entity(self, model: UserModel) -> User:
        return User(
            id=UserId(model.id),
            name=model.name,
            surname=model.surname,
        )
