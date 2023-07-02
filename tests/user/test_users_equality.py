from uuid import uuid4

import factory
from assertpy import assert_that

from python_starter_project.user import User


class UserFactory(factory.Factory):  # type: ignore[misc]
    class Meta:
        model = User

    id = factory.LazyFunction(uuid4)
    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")


class TestUsersEquality:
    def test_two_users_with_the_same_id_should_be_equal(self) -> None:
        id = uuid4()

        user1 = UserFactory.build(id=id)
        user2 = UserFactory.build(id=id)

        assert_that(user1).is_equal_to(user2)

    def test_two_users_with_different_ids_should_not_be_equal(self) -> None:
        user1 = UserFactory.build(name="name", surname="surname")
        user2 = UserFactory.build(name="name", surname="surname")

        assert_that(user1).is_not_equal_to(user2)
