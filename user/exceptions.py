from shared.domain_exception import DomainException


class NoUserFoundException(DomainException):
    CODE = "NO_USER_FOUND"
