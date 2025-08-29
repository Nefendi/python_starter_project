from uuid import UUID

from sqlalchemy.dialects.postgresql import UUID as PSQL_UUID
from sqlalchemy.orm import Mapped, mapped_column

from python_starter_project.database import Base, TimestampsMixin


class UserModel(Base, TimestampsMixin):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(PSQL_UUID(as_uuid=True), primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
