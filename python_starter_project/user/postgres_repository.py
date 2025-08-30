from typing import TypedDict, override

from sqlalchemy import select, update

from ..database import BaseRepository
from .entity import User, UserId
from .exceptions import NoUserFoundException
from .model import UserModel
from .repository import UserRepository


class _UserFieldsToUpdate(TypedDict):
    name: str
    surname: str


class UserPostgresRepository(UserRepository, BaseRepository):
    @override
    def add(self, user: User) -> None:
        user_to_add = self._entity_to_model(user)

        self.session.add(user_to_add)
        self.session.flush([user_to_add])

    @override
    def update(self, user: User) -> User:
        # NOTE: Could be simplified if the entity was an instance of an
        # SQLAlchemy model, but I have separated those two things.
        # This method would be redundant then, because the changes done
        # on the model would automatically get persisted after a transaction
        # has been committed.
        stmt = (
            update(UserModel)
            .where(UserModel.id == user.id.as_uuid)
            .values(self._fields_to_update(user))
            .returning(UserModel)
        )

        updated_user = self.session.scalar(stmt)

        if updated_user is None:
            raise NoUserFoundException(user.id)

        return self._model_to_entity(updated_user)

    @override
    def get_by_id(self, user_id: UserId) -> User:
        stmt = select(UserModel).where(UserModel.id == user_id.as_uuid)

        retrieved_user = self.session.scalar(stmt)

        if not retrieved_user:
            raise NoUserFoundException(user_id)

        return self._model_to_entity(retrieved_user)

    @override
    def get_all(self) -> list[User]:
        stmt = select(UserModel)

        retrieved_users = self.session.scalars(stmt)

        return [self._model_to_entity(user) for user in retrieved_users]

    def _entity_to_model(self, entity: User) -> UserModel:
        return UserModel(id=entity.id.as_uuid, name=entity.name, surname=entity.surname)

    def _model_to_entity(self, model: UserModel) -> User:
        return User(
            id=UserId(model.id),
            name=model.name,
            surname=model.surname,
        )

    def _fields_to_update(self, entity: User) -> _UserFieldsToUpdate:
        return _UserFieldsToUpdate(name=entity.name, surname=entity.surname)
