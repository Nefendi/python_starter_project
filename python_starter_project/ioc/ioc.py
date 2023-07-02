from lagom import Container

from python_starter_project.user.repository import (
    UserPostgresRepository,
    UserRepositoryInterface,
)

container = Container()

container[UserRepositoryInterface] = UserPostgresRepository  # type: ignore[type-abstract]
