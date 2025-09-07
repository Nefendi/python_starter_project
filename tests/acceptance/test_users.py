from datetime import date
from uuid import uuid4

import pytest
import time_machine
from assertpy import assert_that
from fastapi import status

from .steps import Steps

# WARN: The three tests below are *probably* terrible examples of acceptance tests,
# but this project does not model any relevant business processes which are not
# strictly related to CRUD.

DATE = date(2000, 1, 1)


@pytest.mark.slow
class TestUsers:
    @time_machine.travel(DATE)
    def test_should_be_able_to_get_created_user(self, steps: Steps) -> None:
        response = steps.create_user()

        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)
        assert_that(response.headers["Content-Type"]).is_equal_to("application/json")

        data = response.json()
        user_id = data["id"]

        response = steps.get_user_by_id(user_id)

        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.headers["Content-Type"]).is_equal_to("application/json")

        assert_that(data["name"]).is_equal_to("Vernon")
        assert_that(data["surname"]).is_equal_to("Vaughn")
        assert_that(data["age"]).is_equal_to(29)

    @time_machine.travel(DATE)
    def test_should_be_able_to_see_created_user_in_list_of_all_users(
        self, steps: Steps
    ) -> None:
        response = steps.create_user(
            name="Eric", surname="Evans", date_of_birth="1960-05-08"
        )
        user_id = response.json()["id"]

        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)
        assert_that(response.headers["Content-Type"]).is_equal_to("application/json")

        data = response.json()

        response = steps.get_all_users()

        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.headers["Content-Type"]).is_equal_to("application/json")
        assert_that(
            {
                "id": user_id,
                "name": "Eric",
                "surname": "Evans",
                "age": 39,
            }
        ).is_in(data)

    def test_should_fail_gracefully_when_getting_user_who_does_not_exist(
        self, steps: Steps
    ) -> None:
        response = steps.get_user_by_id(uuid4())
        data = response.json()

        assert_that(response.status_code).is_equal_to(status.HTTP_404_NOT_FOUND)
        assert_that(response.headers["Content-Type"]).is_equal_to("application/json")
        assert_that(data).is_equal_to({"message": "A user with this id does not exist"})

    @time_machine.travel(DATE)
    def test_should_be_able_update_already_existing_user(self, steps: Steps) -> None:
        response = steps.create_user()

        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)
        assert_that(response.headers["Content-Type"]).is_equal_to("application/json")

        data = response.json()
        user_id = data["id"]

        response = steps.update_user(
            user_id=user_id, name="Bjarne", surname="Stroustrup"
        )

        data = response.json()

        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.headers["Content-Type"]).is_equal_to("application/json")

        assert_that(data["name"]).is_equal_to("Bjarne")
        assert_that(data["surname"]).is_equal_to("Stroustrup")
        assert_that(data["age"]).is_equal_to(29)
