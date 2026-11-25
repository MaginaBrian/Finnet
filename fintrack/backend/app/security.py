"""JWT creation and the `login_required` decorator.

Password hashing lives on the User model.
"""
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, g, request

from .errors import ApiError
from .extensions import db
from .models import User


def create_token(user: User) -> str:
    now = datetime.now(timezone.utc)
    claims = {
        "sub": str(user.id),
        "iat": now,
        "exp": now + timedelta(minutes=current_app.config["JWT_EXPIRES_MINUTES"]),
    }
    return jwt.encode(claims, current_app.config["SECRET_KEY"], algorithm="HS256")


def _unauthorized(message: str) -> ApiError:
    return ApiError(401, "unauthorized", message)


def login_required(view):
    """Require `Authorization: Bearer <jwt>`; exposes the user as g.current_user."""

    @wraps(view)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        scheme, _, token = header.partition(" ")
        if scheme.lower() != "bearer" or not token:
            raise _unauthorized("Missing or malformed Authorization header.")
        try:
            claims = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise _unauthorized("Your session has expired. Please sign in again.")
        except jwt.InvalidTokenError:
            raise _unauthorized("Invalid authentication token.")
        user = db.session.get(User, int(claims["sub"]))
        if user is None:
            raise _unauthorized("Account no longer exists.")
        g.current_user = user
        return view(*args, **kwargs)

    return wrapper
