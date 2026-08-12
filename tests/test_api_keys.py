from app.security.api_keys import (
    generate_api_key,
    hash_api_key,
)


def test_generated_api_key_has_polytext_prefix():
    key = generate_api_key()

    assert key.startswith("poly_sk_")


def test_generated_api_keys_are_unique():
    first = generate_api_key()
    second = generate_api_key()

    assert first != second


def test_api_key_hash_is_deterministic():
    key = "poly_sk_example"

    assert hash_api_key(key) == hash_api_key(key)


def test_hash_does_not_equal_plaintext_key():
    key = generate_api_key()

    assert hash_api_key(key) != key
