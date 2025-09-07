from datetime import date, timedelta

from assertpy import assert_that

from python_starter_project.user import User, UserId

# WARN: Those tests are kind of stupid, but I wanted to show how to
# unit test very simple things.


class TestUsersEquality:
    def test_two_users_with_the_same_id_should_be_equal(self) -> None:
        id = UserId.new_one()

        user1 = self._user(id=id, name="A", surname="AA", date_of_birth=date.today())
        user2 = self._user(
            id=id,
            name="B",
            surname="BB",
            date_of_birth=date.today() - timedelta(days=365),
        )

        assert_that(user1).is_equal_to(user2)

    def test_two_users_with_different_ids_should_not_be_equal(self) -> None:
        user1 = self._user(
            id=UserId.new_one(), name="A", surname="AA", date_of_birth=date.today()
        )
        user2 = self._user(
            id=UserId.new_one(), name="A", surname="AA", date_of_birth=date.today()
        )

        assert_that(user1).is_not_equal_to(user2)

    def _user(self, id: UserId, name: str, surname: str, date_of_birth: date) -> User:
        return User(id=id, name=name, surname=surname, date_of_birth=date_of_birth)
