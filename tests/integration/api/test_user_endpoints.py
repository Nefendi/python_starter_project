from uuid import uuid4

from assertpy import assert_that
from fastapi import status
from fastapi.testclient import TestClient


class TestUserEndpoints:
    def test_should_be_able_to_add_user(self, client: TestClient) -> None:
        response = client.post("users/", json={"name": "Martin", "surname": "Fowler"})

        data = response.json()
        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)
        assert_that(response.headers["Content-Type"]).is_equal_to("application/json")

        assert_that(data).contains("id")
        assert_that(data["name"]).is_equal_to("Martin")
        assert_that(data["surname"]).is_equal_to("Fowler")
