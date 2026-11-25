from flask import Blueprint, request

from app.extensions import db
from app.models.user import User
from app.services.auth_service import authenticate, register_user
from app.utils.decorators import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
)
from app.utils.responses import APIError, ok

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    user = register_user(data.get("name"), data.get("email"), data.get("password"))
    return ok(_token_payload(user), 201)


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    user = authenticate(data.get("email"), data.get("password"))
    return ok(_token_payload(user))


@auth_bp.post("/refresh")
def refresh():
    payload = decode_token("refresh")
    user = db.session.get(User, int(payload["sub"]))
    if user is None:
        raise APIError("User not found", 401)
    return ok({"access_token": create_access_token(user.id)})


@auth_bp.get("/me")
def me():
    return ok(get_current_user().to_dict())


def _token_payload(user):
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "user": user.to_dict(),
    }
