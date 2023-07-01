from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, scoped_session, sessionmaker

from python_starter_project.database.settings import DbSettings

engine = create_engine(DbSettings().URL)

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
