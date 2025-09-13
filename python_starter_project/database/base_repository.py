from sqlalchemy.ext.asyncio import AsyncSession

from .transaction import _session_ctx_var  # pyright: ignore[reportPrivateUsage]


class BaseRepository:
    @property
    def session(self) -> AsyncSession:
        session = _session_ctx_var.get()

        if session is None:
            raise RuntimeError(
                "A transaction has not been started. Maybe you have forgotten to apply the `transactional` decorator?"
            )

        return session
