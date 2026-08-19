import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from uuid import uuid4


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a local PolyText user and provision "
            "an API key for the Playground."
        ),
    )

    parser.add_argument(
        "--name",
        default="Local Developer",
        help="Display name for the local user.",
    )

    parser.add_argument(
        "--email",
        default=None,
        help=(
            "Email for the local user. Defaults to a "
            "unique local-*@example.com address."
        ),
    )

    parser.add_argument(
        "--api-url",
        default="http://localhost:8000",
        help="Base URL of the running PolyText API.",
    )

    return parser.parse_args()


def load_admin_key() -> str | None:
    env_path = Path(__file__).resolve().parent.parent / ".env"

    if not env_path.exists():
        return None

    for line in env_path.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        key, _, value = line.partition("=")

        if key.strip() == "POLYTEXT_ADMIN_KEY":
            return value.strip().strip('"').strip("'") or None

    return None


def request_json(
    url: str,
    *,
    method: str = "GET",
    body: dict | None = None,
    headers: dict | None = None,
) -> dict:
    data = (
        json.dumps(body).encode("utf-8")
        if body is not None
        else None
    )

    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Content-Type": "application/json",
            **(headers or {}),
        },
    )

    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")

        print(
            f"Request to {url} failed "
            f"({error.code}): {detail}",
            file=sys.stderr,
        )
        raise SystemExit(1) from error
    except urllib.error.URLError as error:
        print(
            f"Could not reach {url}: {error.reason}",
            file=sys.stderr,
        )
        raise SystemExit(1) from error


def main() -> None:
    args = parse_args()

    admin_key = load_admin_key()

    if not admin_key:
        print(
            "POLYTEXT_ADMIN_KEY is not set.\n"
            "Add it to the repository's .env file first.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    email = (
        args.email
        or f"local-{uuid4().hex[:10]}@example.com"
    )

    api_url = args.api_url.rstrip("/")

    print("\nCreating local PolyText user...")

    user = request_json(
        f"{api_url}/v1/users",
        method="POST",
        body={
            "name": args.name,
            "email": email,
        },
    )

    user_id = user["id"]

    print(
        f"Created user {user_id} ({user['email']})."
    )

    print("Creating API key...")

    key_response = request_json(
        f"{api_url}/v1/users/{user_id}/keys",
        method="POST",
        headers={
            "X-PolyText-Admin-Key": admin_key,
        },
    )

    api_key = key_response["key"]

    print("\nAPI key created successfully.\n")

    print(api_key)

    print(
        "\nThis plaintext key is shown only once."
    )

    print(
        "\nPaste it into the PolyText Playground:"
    )

    print("http://localhost:3000\n")


if __name__ == "__main__":
    main()
