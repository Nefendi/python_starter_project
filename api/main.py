from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from shared.domain_exception import DomainException

app = FastAPI()


@app.exception_handler(DomainException)
def domain_exception_handler(_request: Request, _exc: DomainException) -> JSONResponse:
    return JSONResponse(
        content={"message": "Something went wrong"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
