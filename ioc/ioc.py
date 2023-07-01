from lagom import Container

from user.repository import UserPostgresRepository, UserRepositoryInterface

container = Container()

container[UserRepositoryInterface] = UserPostgresRepository
