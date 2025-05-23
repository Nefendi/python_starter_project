from collections.abc import Callable
from typing import Any

from assertpy import assert_that
from fastapi import status
from fastapi.testclient import TestClient

from python_starter_project.shared import DomainException
from python_starter_project.user import UserFacade


class TestApi:
    def test_should_fail_gracefully_when_a_domain_exception_is_thrown(
        self, client: TestClient, when: Callable[[Any], Any]
    ) -> None:
        when(UserFacade).get_all().thenRaise(DomainException)

        response = client.get("users/")

        assert_that(response.status_code).is_equal_to(
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        assert_that(response.headers["Content-Type"]).is_equal_to("application/json")
        assert_that(response.json()).is_equal_to({"message": "Something went wrong"})
