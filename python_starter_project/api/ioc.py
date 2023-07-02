from typing import Any, TypeVar, cast

from fastapi import Depends, Request

from python_starter_project.ioc import container

# NOTE: FastAPI integration from lagom can also be used:
# from lagom.integrations.fast_api import FastApiIntegration
# deps = FastApiIntegration(container)
# lagom_depends = deps.depends

T = TypeVar("T")


# pylint: disable=invalid-name
def Inject(dependency: type[T]) -> T:
    def inject(_request: Request) -> Any:
        return container.resolve(dependency)

    return cast(T, Depends(inject))
