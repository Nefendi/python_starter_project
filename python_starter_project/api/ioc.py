from typing import Any, cast

from fastapi import Depends, Request

from python_starter_project import container as container_assembler

container = container_assembler.build()

# NOTE: FastAPI integration from lagom can also be used:
# from lagom.integrations.fast_api import FastApiIntegration
# deps = FastApiIntegration(container)
# lagom_depends = deps.depends


def Inject[T](dependency: type[T]) -> T:
    def inject(request: Request) -> Any:
        return request.app.state.container.resolve(dependency)

    return cast(T, Depends(inject))
