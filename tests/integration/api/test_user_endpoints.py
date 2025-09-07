from datetime import date
from uuid import uuid4

from assertpy import assert_that
from fastapi import status
from fastapi.testclient import TestClient

from .stubs import NOT_EXISTENT_USER_ID


class TestUserEndpoints:
    def test_should_be_able_to_add_user(self, client: TestClient) -> None:
        # NOTE: Only the shape of the input data matters, not the values, because the
        # dependencies are stubbed.
        response = client.post(
            "users/",
            json={"name": "", "surname": "", "date_of_birth": date.today().isoformat()},
        )
        data = response.json()

        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)
        assert_that(response.headers["Content-Type"]).is_equal_to("application/json")

        assert_that(data).contains("id")
        assert_that(data["name"]).is_equal_to("Martin")
        assert_that(data["surname"]).is_equal_to("Fowler")
        assert_that(data["age"]).is_equal_to(25)

    def test_should_be_able_to_get_user(self, client: TestClient) -> None:
        response = client.get(f"users/{uuid4()}")
        data = response.json()

        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.headers["Content-Type"]).is_equal_to("application/json")

        assert_that(data).contains("id")
        assert_that(data["name"]).is_equal_to("Martin")
        assert_that(data["surname"]).is_equal_to("Fowler")
        assert_that(data["age"]).is_equal_to(25)

    def test_should_fail_when_getting_user_that_does_not_exist(
        self, client: TestClient
    ) -> None:
        response = client.get(f"users/{NOT_EXISTENT_USER_ID.as_uuid}")
        data = response.json()

        assert_that(response.status_code).is_equal_to(status.HTTP_404_NOT_FOUND)
        assert_that(response.headers["Content-Type"]).is_equal_to("application/json")

        assert_that(data["message"]).is_equal_to("A user with this id does not exist")

    def test_should_be_able_to_get_all_users(self, client: TestClient) -> None:
        response = client.get("users/")
        data = response.json()

        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.headers["Content-Type"]).is_equal_to("application/json")

        assert_that(data).is_length(1)
        assert_that(data[0]).contains("id")
        assert_that(data[0]["name"]).is_equal_to("Martin")
        assert_that(data[0]["surname"]).is_equal_to("Fowler")
        assert_that(data[0]["age"]).is_equal_to(25)

    def test_should_be_able_to_update_user(self, client: TestClient) -> None:
        response = client.put(f"users/{uuid4()}", json={"name": "", "surname": ""})
        data = response.json()

        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.headers["Content-Type"]).is_equal_to("application/json")

        assert_that(data).contains("id")
        assert_that(data["name"]).is_equal_to("Martin")
        assert_that(data["surname"]).is_equal_to("Fowler")
        assert_that(data["age"]).is_equal_to(25)

    def test_should_fail_when_updating_user_that_does_not_exist(
        self, client: TestClient
    ) -> None:
        response = client.put(
            f"users/{NOT_EXISTENT_USER_ID.as_uuid}", json={"name": "", "surname": ""}
        )
        data = response.json()

        assert_that(response.status_code).is_equal_to(status.HTTP_404_NOT_FOUND)
        assert_that(response.headers["Content-Type"]).is_equal_to("application/json")

        assert_that(data["message"]).is_equal_to("A user with this id does not exist")
