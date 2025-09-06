from collections.abc import Callable
from contextvars import ContextVar, Token
from functools import wraps
from types import TracebackType
from typing import overload

from sqlalchemy.engine.interfaces import IsolationLevel
from sqlalchemy.orm import (
    Session,
    SessionTransaction,
)

from .db import get_session

_session_ctx_var: ContextVar[Session | None] = ContextVar(
    "_session_ctx_var", default=None
)

ENGINE_DEFAULT = None

type _IsolationLevel = IsolationLevel | None


class _TransactionHelper:
    _session: Session
    _savepoint: SessionTransaction
    _is_nested: bool
    _isolation_level: _IsolationLevel
    _token: Token[Session | None]

    def __init__(self, isolation_level: _IsolationLevel) -> None:
        session = _session_ctx_var.get()

        if session is None:
            session = get_session()
            self._token = _session_ctx_var.set(session)

        self._session = session
        self._is_nested = session.in_transaction()
        self._isolation_level = isolation_level

    def __enter__(self) -> Session | SessionTransaction:
        if self._is_nested:
            self._savepoint = self._session.begin_nested()
            return self._savepoint
        else:
            self._session.begin()

            if self._isolation_level is not ENGINE_DEFAULT:
                self._session.connection(
                    execution_options={"isolation_level": self._isolation_level}
                )

            return self._session

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        # There was no exception
        if exc_type is None:
            if self._is_nested:
                self._savepoint.commit()
            else:
                self._session.commit()
                self._session.close()
        # There was an exception
        elif self._is_nested:
            self._savepoint.rollback()
        # There was an exception
        else:
            self._session.rollback()
            self._session.close()

        if not self._is_nested:
            _session_ctx_var.reset(self._token)


@overload
def transactional[ReturnType, **Params](
    func: Callable[Params, ReturnType],
) -> Callable[Params, ReturnType]: ...


@overload
def transactional[ReturnType, **Params](
    func: None = ...,
    isolation_level: _IsolationLevel = ENGINE_DEFAULT,
) -> Callable[[Callable[Params, ReturnType]], Callable[Params, ReturnType]]: ...


def transactional[ReturnType, **Params](
    func: Callable[Params, ReturnType] | None = None,
    isolation_level: _IsolationLevel = ENGINE_DEFAULT,
) -> (
    Callable[[Callable[Params, ReturnType]], Callable[Params, ReturnType]]
    | Callable[Params, ReturnType]
):
    def inner(
        func: Callable[Params, ReturnType],
    ) -> Callable[Params, ReturnType]:
        @wraps(func)
        def wrapper(*args: Params.args, **kwargs: Params.kwargs) -> ReturnType:
            with _TransactionHelper(isolation_level=isolation_level):
                return func(*args, **kwargs)

        return wrapper

    if func is None:
        return inner

    return inner(func)
