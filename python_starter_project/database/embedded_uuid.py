from typing import Any, Protocol, Self, cast, final, override
from uuid import UUID

from sqlalchemy import Dialect, types

# Stolen from: https://github.com/DomainDrivers/dd-python/blob/a21f3809ea7677ef907c3e0a7e27a2615bc884b6/smartschedule/shared/sqlalchemy_extensions.py#L25


class EmbeddableUUID(Protocol):
    def __init__(self, uuid: UUID, *args: Any, **kwargs: Any) -> None: ...

    @property
    def as_uuid(self) -> UUID: ...


@final
class EmbeddedUUID[T: EmbeddableUUID](types.TypeDecorator[T]):
    """Manages identifiers as UUIDs in the database.

    Type is expected to have a `as_uuid` attribute that is a UUID.
    `.as_uuid` can be read-only, e.g. property.

    It must be possible for the type to be constructed with
    a single argument of UUID type.
    """

    impl = types.UUID(as_uuid=True)
    cache_ok = True

    _type: type[T] | None

    @override
    def __class_getitem__(cls, type_: type[T]) -> Self:
        specialized_class = type(
            f"EmbeddedUUID[{type_.__name__}]",
            (cls,),
            {"_type": type_, "cache_ok": True},
        )
        return cast(Self, specialized_class)

    @override
    def process_bind_param(self, value: T | None, dialect: Dialect) -> UUID | None:
        if value is not None:
            return value.as_uuid

        return value

    @override
    def process_result_value(self, value: UUID | None, dialect: Dialect) -> T | None:
        if self._type is None:
            raise RuntimeError("Type not set, use EmbeddedUUID[Type]")

        if value is not None:
            return self._type(value)

        return value
