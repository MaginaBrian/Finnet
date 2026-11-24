from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)

from app.extensions import db
from app.models.user import User
from app.services.auth_service import authenticate, register_user
from app.utils.decorators import get_current_user
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
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    if identity is None:
        raise APIError("Authentication required", 401)
    user = db.session.get(User, int(identity))
    if user is None:
        raise APIError("User not found", 401)
    return ok({"access_token": create_access_token(identity=str(user.id))})


@auth_bp.get("/me")
def me():
    return ok(get_current_user().to_dict())


def _token_payload(user):
    identity = str(user.id)
    return {
        "access_token": create_access_token(identity=identity),
        "refresh_token": create_refresh_token(identity=identity),
        "user": user.to_dict(),
    }
