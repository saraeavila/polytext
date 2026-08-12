from app.services.api_user import (
    APIUserAlreadyExistsError,
    APIUserService,
)


class FakeAPIUserRepository:
    def __init__(self):
        self.users = {}

    def get_by_email(self, email: str):
        return self.users.get(email)

    def create(self, name: str, email: str):
        user = {
            "name": name,
            "email": email,
        }

        self.users[email] = user
        return user


def test_create_api_user():
    repository = FakeAPIUserRepository()
    service = APIUserService(repository=repository)

    user = service.create_user(
        name="Sara",
        email="sara@example.com",
    )

    assert user["name"] == "Sara"
    assert user["email"] == "sara@example.com"


def test_duplicate_api_user_is_rejected():
    repository = FakeAPIUserRepository()

    repository.create(
        name="Sara",
        email="sara@example.com",
    )

    service = APIUserService(repository=repository)

    try:
        service.create_user(
            name="Another Sara",
            email="sara@example.com",
        )

        assert False, "Expected APIUserAlreadyExistsError"

    except APIUserAlreadyExistsError:
        pass
