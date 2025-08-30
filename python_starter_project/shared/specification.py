from __future__ import annotations

from abc import ABC, abstractmethod
from typing import NamedTuple, final, override


class Specification[T](ABC):
    @abstractmethod
    def is_satisfied_by(self, obj: T) -> bool:
        pass

    @final
    def __and__(self, other_spec: Specification[T]) -> _AndSpecification[T]:
        return _AndSpecification(self, other_spec)

    @final
    def __or__(self, other_spec: Specification[T]) -> _OrSpecification[T]:
        return _OrSpecification(self, other_spec)

    @final
    def __xor__(self, other_spec: Specification[T]) -> _XorSpecification[T]:
        return _XorSpecification(self, other_spec)

    @final
    def __invert__(self) -> _InvertSpecification[T]:
        return _InvertSpecification(self)


class _UnarySpecification[T](Specification[T], ABC):
    _spec: Specification[T]

    def __init__(self, spec: Specification[T]) -> None:
        self._spec = spec

    @property
    def spec(self) -> Specification[T]:
        return self._spec


class _Both[T](NamedTuple):
    left: Specification[T]
    right: Specification[T]


class _BinarySpecification[T](Specification[T], ABC):
    _left: Specification[T]
    _right: Specification[T]

    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self._left = left
        self._right = right

    @property
    def left(self) -> Specification[T]:
        return self._left

    @property
    def right(self) -> Specification[T]:
        return self._right

    @property
    def both(self) -> _Both[T]:
        return _Both(self._left, self._right)


class _CompositeSpecification[T](Specification[T], ABC):
    _specs: tuple[Specification[T], ...]

    def __init__(self, *specs: Specification[T]) -> None:
        self._specs = specs

    @property
    def specs(self) -> tuple[Specification[T], ...]:
        return self._specs


class _AndSpecification[T](_BinarySpecification[T]):
    @override
    def is_satisfied_by(self, obj: T) -> bool:
        return self._left.is_satisfied_by(obj) and self._right.is_satisfied_by(obj)


class _OrSpecification[T](_BinarySpecification[T]):
    @override
    def is_satisfied_by(self, obj: T) -> bool:
        return self._left.is_satisfied_by(obj) or self._right.is_satisfied_by(obj)


class _XorSpecification[T](_BinarySpecification[T]):
    @override
    def is_satisfied_by(self, obj: T) -> bool:
        return self._left.is_satisfied_by(obj) ^ self._right.is_satisfied_by(obj)


class _InvertSpecification[T](_UnarySpecification[T]):
    @override
    def is_satisfied_by(self, obj: T) -> bool:
        return not self._spec.is_satisfied_by(obj)


class _CompositeAndSpecification[T](_CompositeSpecification[T]):
    @override
    def is_satisfied_by(self, obj: T) -> bool:
        return all(spec.is_satisfied_by(obj) for spec in self._specs)


class _CompositeOrSpecification[T](_CompositeSpecification[T]):
    @override
    def is_satisfied_by(self, obj: T) -> bool:
        return any(spec.is_satisfied_by(obj) for spec in self._specs)


### Utility functions ###


def and_spec[T](
    left: Specification[T], right: Specification[T]
) -> _AndSpecification[T]:
    return _AndSpecification(left, right)


def or_spec[T](left: Specification[T], right: Specification[T]) -> _OrSpecification[T]:
    return _OrSpecification(left, right)


def xor_spec[T](
    left: Specification[T], right: Specification[T]
) -> _XorSpecification[T]:
    return _XorSpecification(left, right)


def invert_spec[T](spec: Specification[T]) -> _InvertSpecification[T]:
    return _InvertSpecification(spec)


def composite_and_spec[T](*specs: Specification[T]) -> _CompositeAndSpecification[T]:
    return _CompositeAndSpecification(*specs)


def composite_or_spec[T](*specs: Specification[T]) -> _CompositeOrSpecification[T]:
    return _CompositeOrSpecification(*specs)
