from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

timestamps = (
    Column(
        "created_at",
        TIMESTAMP(timezone=False),
        nullable=False,
        server_default=func.now(),
    ),
    Column(
        "updated_at",
        TIMESTAMP(timezone=False),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
)


class TimestampsMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        server_default=func.now(),
        onupdate=func.now(),
    )
