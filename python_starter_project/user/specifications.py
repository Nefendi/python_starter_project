from typing import ClassVar, override

from python_starter_project.shared import Specification

from .entity import User


class IsAdultSpecification(Specification[User]):
    _ADULT_AGE: ClassVar[int] = 18

    @override
    def is_satisfied_by(self, obj: User) -> bool:
        return obj.age >= self._ADULT_AGE
