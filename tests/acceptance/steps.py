from uuid import UUID

from attrs import define
from fastapi.testclient import TestClient
from httpx import Response


@define
class Steps:
    _client: TestClient

    def create_user(
        self,
        name: str = "Vernon",
        surname: str = "Vaughn",
        date_of_birth: str = "1970-09-07",
    ) -> Response:
        return self._client.post(
            "/users",
            json={"name": name, "surname": surname, "date_of_birth": date_of_birth},
        )

    def get_user_by_id(self, user_id: UUID) -> Response:
        return self._client.get(f"/users/{user_id}")

    def get_all_users(self) -> Response:
        return self._client.get("/users")

    def update_user(self, user_id: UUID, name: str, surname: str) -> Response:
        return self._client.put(
            f"/users/{user_id}", json={"name": name, "surname": surname}
        )
