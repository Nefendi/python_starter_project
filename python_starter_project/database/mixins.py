from datetime import datetime

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
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
