# NOTE: Taken from https://ryan-zheng.medium.com/simplifying-database-interactions-in-python-with-the-repository-pattern-and-sqlalchemy-22baecae8d84


from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    registry,
)

from .settings import DbSettings

_engine = create_async_engine(str(DbSettings().URL))

session_factory = async_sessionmaker(
    bind=_engine, autoflush=False, expire_on_commit=False
)


def get_session() -> AsyncSession:
    return session_factory()


class Base(DeclarativeBase):
    pass


metadata = Base.metadata

mapper_registry = registry(metadata=metadata)
