from collections.abc import Iterator
from typing import override
from uuid import uuid4

import pytest
from attrs import define
from fastapi.testclient import TestClient
from lagom import Container

from python_starter_project import container as container_assembler
from python_starter_project.api.main import app
from python_starter_project.user import (
    UserDTO,
    UserFacade,
    UserId,
)


# NOTE: One could also create a stub for the underlying repository, but
# it's probably better to override the facade to get rid of the transactional
# decorator underneath
@define
class UserFacadeStub(UserFacade):
    @override
    def add(self, name: str, surname: str) -> UserDTO:
        return self._user()

    @override
    def get_by_id(self, id: UserId) -> UserDTO:
        return self._user()

    @override
    def get_all(self) -> list[UserDTO]:
        return [self._user()]

    def _user(self) -> UserDTO:
        return UserDTO(id=uuid4(), name="Martin", surname="Fowler")


@pytest.fixture
def container() -> Container:
    # NOTE: In the integration tests of the API, we don't really want to
    # have the working implementations of the dependencies. We want to
    # only test the endpoints. The testing of the API with production
    # dependencies is done in the acceptance / end-to-end tests.
    container = container_assembler.build().clone()

    container[UserFacade] = UserFacadeStub

    return container


@pytest.fixture
def client(container: Container) -> Iterator[TestClient]:
    old_container: Container = app.state.container

    app.state.container = container

    yield TestClient(app)

    app.state.container = old_container
