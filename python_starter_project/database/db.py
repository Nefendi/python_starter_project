from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, scoped_session, sessionmaker

from .settings import DbSettings

engine = create_engine(str(DbSettings().URL))

session_factory = sessionmaker(bind=engine)

ScopedSession = scoped_session(session_factory)


class Base(DeclarativeBase):
    pass


@contextmanager
def get_session() -> Iterator[Session]:
    session = ScopedSession()

    try:
        yield session
    finally:
        ScopedSession.remove()
