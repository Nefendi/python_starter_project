from typing import override

from sqlalchemy import select

from ..database import BaseRepository
from .entity import User, UserId
from .exceptions import NoUserFoundException
from .model import users
from .repository import UserRepository


class UserPostgresRepository(UserRepository, BaseRepository):
    @override
    def add(self, user: User) -> None:
        self.session.add(user)
        self.session.flush([user])

    @override
    def get_by_id(self, user_id: UserId) -> User:
        stmt = select(User).where(users.c.id == user_id)

        retrieved_user = self.session.scalar(stmt)

        if not retrieved_user:
            raise NoUserFoundException(user_id)

        return retrieved_user

    @override
    def get_all(self) -> list[User]:
        stmt = select(User)

        retrieved_users = self.session.scalars(stmt).all()

        return list(retrieved_users)
