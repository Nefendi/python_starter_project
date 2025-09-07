from sqlalchemy import Column, Date, String, Table

from python_starter_project.database import (
    EmbeddedUUID,
    mapper_registry,
    metadata,
    timestamps,
)

from .entity import User, UserId

# NOTE: Imperative mapping
# It suits DDD more, because we keep the domain model pure and
# we still can make use of SQLAlchemy's Unit of Work pattern.
# For simpler cases, when it is not that important to keep the domain model
# pure, declarative mapping should be used as it produces cleaner and shorter
# code, since there is only one class per database table.
users = Table(
    "users",
    metadata,
    Column("id", EmbeddedUUID[UserId], primary_key=True),
    Column("name", String(), nullable=False),
    Column("surname", String(), nullable=False),
    Column("date_of_birth", Date(), nullable=False),
    *timestamps,
)

mapper_registry.map_imperatively(User, users, properties={"_id": users.c.id})
