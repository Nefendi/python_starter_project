from python_starter_project.shared import DomainException


class NoUserFoundException(DomainException):
    CODE = "NO_USER_FOUND"
