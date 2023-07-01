from abc import ABC, abstractmethod
from typing import Iterator
from uuid import UUID

from database.db import ScopedSession
from user.entity import User
from user.exceptions import NoUserFoundException
from user.model import UserModel


class UserRepositoryInterface(ABC):
    @abstractmethod
    def add(self, user: User) -> None:
        pass

    @abstractmethod
    def get_by_id(self, id: UUID) -> User:
        pass

    @abstractmethod
    def get_all(self) -> Iterator[User]:
        pass


class UserPostgresRepository(UserRepositoryInterface):
    def add(self, user: User) -> None:
        session = ScopedSession()

        user_to_add = self._entity_to_model(user)
        session.add(user_to_add)
        # session.flush()

    def get_by_id(self, id: UUID) -> User:
        session = ScopedSession()

        retrieved_user: UserModel | None = (
            session.query(UserModel).filter_by(id=id).first()
        )

        if not retrieved_user:
            raise NoUserFoundException()

        return self._model_to_entity(retrieved_user)

    def get_all(self) -> Iterator[User]:
        session = ScopedSession()

        retrieved_users = session.query(UserModel).all()

        return (self._model_to_entity(user) for user in retrieved_users)

    def _entity_to_model(self, entity: User) -> UserModel:
        return UserModel(id=entity.id, name=entity.name, surname=entity.surname)

    def _model_to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            name=model.name,
            surname=model.surname,
        )
