# NOTE: Taken from https://ryan-zheng.medium.com/simplifying-database-interactions-in-python-with-the-repository-pattern-and-sqlalchemy-22baecae8d84


from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    registry,
    sessionmaker,
)

from .settings import DbSettings

_engine = create_engine(str(DbSettings().URL))

session_factory = sessionmaker(bind=_engine, autoflush=False, expire_on_commit=False)


def get_session() -> Session:
    return session_factory()


class Base(DeclarativeBase):
    pass


metadata = Base.metadata

mapper_registry = registry(metadata=metadata)
