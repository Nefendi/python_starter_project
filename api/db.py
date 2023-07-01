from typing import Iterator

from sqlalchemy.orm import Session

from database.db import get_session


def db_session() -> Iterator[Session]:
    with get_session() as session:
        yield session
