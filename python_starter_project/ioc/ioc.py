from lagom import Container

from python_starter_project.user import UserPostgresRepository, UserRepository

container = Container()

container[UserRepository] = UserPostgresRepository  # type: ignore[type-abstract]
