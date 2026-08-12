from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.api_user import APIUser


class APIUserRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_by_email(self, email: str) -> APIUser | None:
        statement = select(APIUser).where(
            APIUser.email == email
        )

        return self._db.scalar(statement)

    def create(
        self,
        name: str,
        email: str,
    ) -> APIUser:
        user = APIUser(
            name=name,
            email=email,
        )

        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)

        return user
