from typing import Iterator

from sqlalchemy.orm import Session

from python_starter_project.database import get_session


def db_session() -> Iterator[Session]:
    with get_session() as session:
        yield session
