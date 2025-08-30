from typing import override

from sqlalchemy import select, update

from ..database import BaseRepository
from .entity import User, UserId
from .exceptions import NoUserFoundException
from .model import UserModel
from .repository import UserRepository


class UserPostgresRepository(UserRepository, BaseRepository):
    @override
    def add(self, user: User) -> None:
        user_to_add = self._entity_to_model(user)

        self.session.add(user_to_add)
        self.session.flush([user_to_add])

    @override
    def update(self, user: User) -> None:
        # NOTE: Could be simplified if the entity was an instance of an
        # SQLAlchemy model, but I have separated those two things.
        # This method would be redundant then, because the changes done
        # on the model would automatically get persisted after a transaction
        # has been committed.
        user_to_update = self._entity_to_model(user)

        stmt = (
            update(UserModel)
            .where(UserModel.id == user_to_update.id)
            .values(name=user_to_update.name, surname=user_to_update.surname)
        )

        self.session.execute(stmt)
        self.session.flush([user_to_update])

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
