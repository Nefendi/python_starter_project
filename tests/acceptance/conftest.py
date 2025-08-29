import os
import pathlib
from collections.abc import Iterator

import alembic.command
import alembic.config
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from testcontainers.postgres import PostgresContainer

from python_starter_project.api.main import app
from python_starter_project.database import session_factory


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


# Stolen from: https://github.com/Enforcer/bottega-ddd-modulith/blob/main/tests/conftest.py
# WARN: This setup work probably only for Postgres. You need to adjust it for different databases
@pytest.fixture(autouse=True)
def _setup_test_database() -> Iterator[None]:
    with PostgresContainer(
        image="postgres:15",
        port=5432,
        user="python_starter_project",
        password="password",
    ) as postgres:
        test_db_engine = create_engine(postgres.get_connection_url(), echo=True)

        session_factory.configure(bind=test_db_engine)

        with test_db_engine.begin():
            testing_db_url = test_db_engine.url

            password = testing_db_url.password if testing_db_url.password else ""

            # NOTE: Needed for alembic's migrations to run against the test database.
            # The configuration of engine and session_factory is enough for the code
            # to run properly, but alembic needs this environment variable.
            os.environ["DB_CONFIG_URL"] = str(testing_db_url).replace("***", password)

            script_location = (
                pathlib.Path(__file__).parent.parent.parent / "migrations/"
            )

            config = alembic.config.Config()

            config.set_main_option("script_location", str(script_location))

            alembic.command.upgrade(config=config, revision="head")

            yield


# Stolen from: https://github.com/Enforcer/bottega-ddd-modulith/blob/main/tests/conftest.py
# WARN: This setup work probably only for Postgres. You need to adjust it for different databases
# @pytest.fixture(scope="session", autouse=True)
# def _setup_test_database() -> Iterator[None]:
#     if (prod_db_url := engine.url.database) is None:
#         raise Exception(
#             "There is something wrong with the engine for production database!"
#         )

#     test_db_name = prod_db_url + "_test"

#     with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
#         connection.execute(text(f"DROP DATABASE IF EXISTS {test_db_name}"))
#         connection.execute(text(f"CREATE DATABASE {test_db_name}"))

#     testing_db_url = engine.url.set(database=test_db_name)

#     test_db_engine = create_engine(testing_db_url, echo=True)

#     session_factory.configure(bind=test_db_engine)

#     password = testing_db_url.password if testing_db_url.password else ""

#     # NOTE: Needed for alembic's migrations to run against the test database.
#     # The configuration of engine and session_factory is enough for the code
#     # to run properly, but alembic needs this environment variable.
#     os.environ["DB_CONFIG_URL"] = str(testing_db_url).replace("***", password)

#     script_location = (
#         pathlib.Path(__file__).parent.parent.parent
#         / "migrations"
#     )

#     config = alembic.config.Config()

#     config.set_main_option("script_location", str(script_location))

#     alembic.command.upgrade(config=config, revision="head")

#     yield

#     test_db_engine.dispose()
