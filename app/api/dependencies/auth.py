from fastapi import Depends, HTTPException, Request, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.models.api_key import APIKey
from app.db.session import get_db
from app.repositories.api_key import APIKeyRepository
from app.security.api_keys import hash_api_key


bearer_scheme = HTTPBearer(auto_error=False)


def require_api_key(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Security(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> APIKey:
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="API key required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    repository = APIKeyRepository(db)

    api_key = repository.get_by_hash(
        hash_api_key(credentials.credentials)
    )

    if api_key is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or revoked API key",
            headers={"WWW-Authenticate": "Bearer"},
        )

    request.state.api_key_id = api_key.id

    return api_key
