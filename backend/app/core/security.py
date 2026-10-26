from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
from datetime import UTC, datetime, timedelta

from app.core.config import get_settings

SESSION_COOKIE_NAME = "buildlog_session"
SESSION_MAX_AGE_SECONDS = 7 * 24 * 60 * 60
_process_session_secret = secrets.token_bytes(32)


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)
    return "scrypt$1$" + _b64encode(salt) + "$" + _b64encode(digest)


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, version, salt_text, digest_text = encoded.split("$")
        if algorithm != "scrypt" or version != "1":
            return False
        salt = _b64decode(salt_text)
        expected = _b64decode(digest_text)
        actual = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def create_session_token(user_id: int) -> str:
    expires_at = int((datetime.now(UTC) + timedelta(days=7)).timestamp())
    payload = {"user_id": user_id, "exp": expires_at}
    payload_text = _b64encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signature = _sign(payload_text)
    return f"{payload_text}.{signature}"


def read_session_token(token: str) -> int | None:
    try:
        payload_text, signature = token.split(".", 1)
        if not hmac.compare_digest(signature, _sign(payload_text)):
            return None
        payload = json.loads(_b64decode(payload_text))
        if int(payload["exp"]) <= int(datetime.now(UTC).timestamp()):
            return None
        return int(payload["user_id"])
    except (ValueError, TypeError, KeyError, json.JSONDecodeError):
        return None


def session_cookie_options() -> dict[str, object]:
    settings = get_settings()
    return {
        "key": SESSION_COOKIE_NAME,
        "httponly": True,
        "samesite": "lax",
        "secure": settings.environment == "production",
        "max_age": SESSION_MAX_AGE_SECONDS,
        "path": "/",
    }


def _sign(value: str) -> str:
    settings = get_settings()
    secret = (
        settings.session_secret.encode("utf-8")
        if settings.session_secret
        else _process_session_secret
    )
    return _b64encode(hmac.new(secret, value.encode("utf-8"), hashlib.sha256).digest())


def _b64encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _b64decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))

