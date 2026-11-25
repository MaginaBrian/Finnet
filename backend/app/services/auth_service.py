from app.errors import ApiError
from app.extensions import db
from app.models import User

def register_user(clean):
    if User.query.filter_by(username=clean["username"]).first():
        raise ApiError(409, "conflict", "Username is already taken.")
    user = User(username=clean["username"], full_name=clean.get("full_name") or "")
    user.set_password(clean["password"])
    db.session.add(user)
    db.session.commit()
    return user

def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password or ""):
        raise ApiError(401, "unauthorized", "Invalid username or password.")
    return user
