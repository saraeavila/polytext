import hashlib
import secrets


API_KEY_PREFIX = "poly_sk_"


def generate_api_key() -> str:
    secret = secrets.token_urlsafe(32)
    return f"{API_KEY_PREFIX}{secret}"


def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(
        api_key.encode("utf-8")
    ).hexdigest()


def get_api_key_prefix(api_key: str) -> str:
    return api_key[:15]
