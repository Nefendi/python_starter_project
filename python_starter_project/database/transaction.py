import enum
from collections.abc import Callable, Coroutine
from contextvars import ContextVar, Token
from functools import wraps
from types import TracebackType
from typing import Any, overload, override

from sqlalchemy.engine.interfaces import IsolationLevel
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from .db import get_session

_session_ctx_var: ContextVar[AsyncSession | None] = ContextVar(
    "_session_ctx_var", default=None
)


class _EngineDefault(enum.Enum):
    """
    Sentinel to indicate the lack of a value when `None` is ambiguous.
    """

    ENGINE_DEFAULT = enum.auto()

    @override
    def __repr__(self) -> str:
        return "ENGINE_DEFAULT"


ENGINE_DEFAULT = _EngineDefault.ENGINE_DEFAULT

type _IsolationLevel = IsolationLevel | _EngineDefault


class _TransactionHelper:
    _session: AsyncSession
    _savepoint: AsyncSessionTransaction
    _is_nested: bool
    _isolation_level: _IsolationLevel
    _token: Token[AsyncSession | None]

    def __init__(self, isolation_level: _IsolationLevel) -> None:
        session = _session_ctx_var.get()

        if session is None:
            session = get_session()
            self._token = _session_ctx_var.set(session)

        self._session = session
        self._is_nested = session.in_transaction()
        self._isolation_level = isolation_level

    async def __aenter__(self) -> AsyncSession | AsyncSessionTransaction:
        if self._is_nested:
            self._savepoint = self._session.begin_nested()
            return self._savepoint
        else:
            self._session.begin()

            if self._isolation_level is not ENGINE_DEFAULT:
                await self._session.connection(
                    execution_options={"isolation_level": self._isolation_level}
                )

            return self._session

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        # There was no exception
        if exc_type is None:
            if self._is_nested:
                await self._savepoint.commit()
            else:
                await self._session.commit()
                await self._session.close()
        # There was an exception
        elif self._is_nested:
            await self._savepoint.rollback()
        # There was an exception
        else:
            await self._session.rollback()
            await self._session.close()

        if not self._is_nested:
            _session_ctx_var.reset(self._token)


@overload
def transactional[ReturnType, **Params](
    func: Callable[Params, Coroutine[Any, Any, ReturnType]],
) -> Callable[Params, Coroutine[Any, Any, ReturnType]]: ...


@overload
def transactional[ReturnType, **Params](
    func: None = ...,
    isolation_level: _IsolationLevel = ENGINE_DEFAULT,
) -> Callable[
    [Callable[Params, Coroutine[Any, Any, ReturnType]]],
    Callable[Params, Coroutine[Any, Any, ReturnType]],
]: ...


def transactional[ReturnType, **Params](
    func: Callable[Params, Coroutine[Any, Any, ReturnType]] | None = None,
    isolation_level: _IsolationLevel = ENGINE_DEFAULT,
) -> (
    Callable[
        [Callable[Params, Coroutine[Any, Any, ReturnType]]],
        Callable[Params, Coroutine[Any, Any, ReturnType]],
    ]
    | Callable[Params, Coroutine[Any, Any, ReturnType]]
):
    def inner(
        func: Callable[Params, Coroutine[Any, Any, ReturnType]],
    ) -> Callable[Params, Coroutine[Any, Any, ReturnType]]:
        @wraps(func)
        async def wrapper(*args: Params.args, **kwargs: Params.kwargs) -> ReturnType:
            async with _TransactionHelper(isolation_level=isolation_level):
                return await func(*args, **kwargs)

        return wrapper

    if func is None:
        return inner

    return inner(func)
