import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
from flask import current_app, request

from app.extensions import db
from app.models.user import User
from app.utils.responses import APIError


def _load_local_env():
    """Load backend/.env without overriding variables already set in the process."""
    path = Path(__file__).resolve().parents[2] / ".env"
    if not path.is_file():
        return
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def create_access_token(identity):
    minutes = int(current_app.config.get("JWT_EXPIRES_MINUTES", 60))
    return _encode(identity, "access", timedelta(minutes=minutes))


def create_refresh_token(identity):
    return _encode(identity, "refresh", timedelta(days=7))


def get_current_user():
    payload = decode_token("access")
    user = db.session.get(User, int(payload["sub"]))
    if user is None:
        raise APIError("User not found", 401)
    return user


def decode_token(expected_type):
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        raise APIError("Authentication required", 401)
    token = header[7:].strip()
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    except jwt.ExpiredSignatureError as exc:
        raise APIError("Token expired", 401) from exc
    except jwt.InvalidTokenError as exc:
        raise APIError("Invalid token", 401) from exc
    if payload.get("type") != expected_type or payload.get("sub") is None:
        raise APIError("Invalid token", 401)
    return payload


def _encode(identity, token_type, lifetime):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(identity),
        "type": token_type,
        "iat": now,
        "exp": now + lifetime,
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
