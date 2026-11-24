from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from app.extensions import db
from app.models.user import User
from app.utils.responses import APIError


def get_current_user():
    verify_jwt_in_request()
    identity = get_jwt_identity()
    if identity is None:
        raise APIError("Authentication required", 401)
    user = db.session.get(User, int(identity))
    if user is None:
        raise APIError("User not found", 401)
    return user
