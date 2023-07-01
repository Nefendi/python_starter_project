from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from user.exceptions import NoUserFoundException


def add_users_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NoUserFoundException)
    def no_user_found_exception_handler(
        _request: Request, _exc: NoUserFoundException
    ) -> JSONResponse:
        return JSONResponse(
            content={"message": "A user with this id does not exist"},
            status_code=status.HTTP_404_NOT_FOUND,
        )
