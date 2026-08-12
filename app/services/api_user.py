from app.db.models.api_user import APIUser
from app.repositories.api_user import APIUserRepository


class APIUserAlreadyExistsError(Exception):
    pass


class APIUserService:
    def __init__(self, repository: APIUserRepository):
        self._repository = repository

    def create_user(
        self,
        name: str,
        email: str,
    ) -> APIUser:
        existing = self._repository.get_by_email(email)

        if existing is not None:
            raise APIUserAlreadyExistsError(
                f"API user with email {email!r} already exists"
            )

        return self._repository.create(
            name=name,
            email=email,
        )
