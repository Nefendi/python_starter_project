from python_starter_project.shared.domain_exception import DomainException


class NoUserFoundException(DomainException):
    CODE = "NO_USER_FOUND"
