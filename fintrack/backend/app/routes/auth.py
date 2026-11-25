from flask import Blueprint

from app.security import create_token, login_required
from app.services.auth_service import authenticate, register_user
from app.services.validation import json_body, validate_credentials
from app.utils.responses import ok

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    user = register_user(validate_credentials(json_body(), registering=True))
    return ok({"access_token": create_token(user), "user": user.to_dict()}, 201)


@auth_bp.post("/login")
def login():
    clean = validate_credentials(json_body(), registering=False)
    user = authenticate(clean["username"], clean["password"])
    return ok({"access_token": create_token(user), "user": user.to_dict()})


@auth_bp.get("/me")
@login_required
def me():
    from flask import g

    return ok(g.current_user.to_dict())
