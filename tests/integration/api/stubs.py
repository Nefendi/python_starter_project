from typing import override
from uuid import uuid4

from python_starter_project.user import (
    NoUserFoundException,
    UserDTO,
    UserFacade,
    UserId,
)

NOT_EXISTENT_USER_ID = UserId.new_one()


# NOTE: One could also create a stub for the underlying repository, but
# it's probably better to override the facade to get rid of the transactional
# decorator underneath
class UserFacadeStub(UserFacade):
    @override
    def add(self, name: str, surname: str) -> UserDTO:
        return self._user()

    @override
    def update(self, user_id: UserId, name: str, surname: str) -> UserDTO:
        if user_id == NOT_EXISTENT_USER_ID:
            raise NoUserFoundException(NOT_EXISTENT_USER_ID)

        return self._user()

    @override
    def get_by_id(self, user_id: UserId) -> UserDTO:
        if user_id == NOT_EXISTENT_USER_ID:
            raise NoUserFoundException(NOT_EXISTENT_USER_ID)

        return self._user()

    @override
    def get_all(self) -> list[UserDTO]:
        return [self._user()]

    def _user(self) -> UserDTO:
        return UserDTO(id=uuid4(), name="Martin", surname="Fowler")
