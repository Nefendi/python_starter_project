from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from lagom import Container

from python_starter_project import container as container_assembler
from python_starter_project.api.main import app
from python_starter_project.user import (
    UserFacade,
)

from .stubs import UserFacadeStub


@pytest.fixture
def container() -> Container:
    # NOTE: In the integration tests of the API, we don't really want to
    # have the working implementations of the dependencies. We want to
    # only test the endpoints. The testing of the API with production
    # dependencies is done in the acceptance / end-to-end tests.
    container = container_assembler.build()

    container[UserFacade] = UserFacadeStub

    return container


@pytest.fixture
def client(container: Container) -> Iterator[TestClient]:
    old_container: Container = app.state.container

    app.state.container = container

    yield TestClient(app)

    app.state.container = old_container
