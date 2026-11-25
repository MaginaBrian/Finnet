from flask import Blueprint, g, jsonify

from ..errors import ApiError
from ..extensions import db
from ..models import User
from ..security import create_token, login_required
from ..services.validation import json_body, validate_credentials

bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@bp.post("/register")
def register():
    data = validate_credentials(json_body(), registering=True)
    if User.query.filter_by(username=data["username"]).first():
        raise ApiError(409, "conflict", "That username is already taken.", {"username": "Already taken."})
    user = User(username=data["username"], full_name=data["full_name"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"token": create_token(user), "user": user.to_dict()}), 201


@bp.post("/login")
def login():
    data = validate_credentials(json_body(), registering=False)
    user = User.query.filter_by(username=data["username"]).first()
    # Same message for unknown user and wrong password: don't reveal which accounts exist.
    if user is None or not user.check_password(data["password"]):
        raise ApiError(401, "invalid_credentials", "Incorrect username or password.")
    return jsonify({"token": create_token(user), "user": user.to_dict()})


@bp.get("/me")
@login_required
def me():
    return jsonify({"user": g.current_user.to_dict()})
