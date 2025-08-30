from uuid import uuid4

from assertpy import assert_that
from fastapi import status
from fastapi.testclient import TestClient

# WARN: The three tests below are *probably* terrible examples of acceptance tests,
# but this project does not model any relevant business processes which are not
# strictly related to CRUD.


class TestUsers:
    def test_should_be_able_to_get_created_user(self, client: TestClient) -> None:
        response = client.post("users/", json={"name": "Vernon", "surname": "Vaughn"})

        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)
        assert_that(response.headers["Content-Type"]).is_equal_to("application/json")

        data = response.json()
        id = data["id"]

        response = client.get(f"users/{id}")

        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.headers["Content-Type"]).is_equal_to("application/json")

        assert_that(data["name"]).is_equal_to("Vernon")
        assert_that(data["surname"]).is_equal_to("Vaughn")

    def test_should_be_able_to_see_created_user_in_list_of_all_users(
        self,
        client: TestClient,
    ) -> None:
        response = client.post("users/", json={"name": "Eric", "surname": "Evans"})
        id = response.json()["id"]

        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)
        assert_that(response.headers["Content-Type"]).is_equal_to("application/json")

        data = response.json()

        response = client.get("users/")

        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.headers["Content-Type"]).is_equal_to("application/json")
        assert_that({"id": id, "name": "Eric", "surname": "Evans"}).is_in(data)

    def test_should_fail_gracefully_when_getting_user_who_does_not_exist(
        self,
        client: TestClient,
    ) -> None:
        response = client.get(f"users/{uuid4()}")
        data = response.json()

        assert_that(response.status_code).is_equal_to(status.HTTP_404_NOT_FOUND)
        assert_that(response.headers["Content-Type"]).is_equal_to("application/json")
        assert_that(data).is_equal_to({"message": "A user with this id does not exist"})
