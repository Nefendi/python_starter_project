from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from python_starter_project.api.users.exception_handlers import (
    add_users_exception_handlers,
)
from python_starter_project.api.users.user import router as user_router
from python_starter_project.shared.domain_exception import DomainException

app = FastAPI()


@app.exception_handler(DomainException)
def domain_exception_handler(_request: Request, _exc: DomainException) -> JSONResponse:
    return JSONResponse(
        content={"message": "Something went wrong"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


app.include_router(user_router)

add_users_exception_handlers(app)