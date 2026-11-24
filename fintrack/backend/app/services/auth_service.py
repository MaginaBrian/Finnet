from app.extensions import db
from app.models.user import User
from app.utils.responses import APIError


def register_user(name, email, password):
    cleaned_name = (name or "").strip()
    cleaned_email = (email or "").strip().lower()
    if not cleaned_name:
        raise APIError("Name is required")
    if "@" not in cleaned_email or "." not in cleaned_email.split("@")[-1]:
        raise APIError("A valid email is required")
    if not password or len(password) < 8:
        raise APIError("Password must be at least 8 characters")
    if User.query.filter_by(email=cleaned_email).first():
        raise APIError("Email is already registered", 409)

    user = User(name=cleaned_name, email=cleaned_email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def authenticate(email, password):
    cleaned_email = (email or "").strip().lower()
    user = User.query.filter_by(email=cleaned_email).first()
    if user is None or not user.check_password(password or ""):
        raise APIError("Invalid email or password", 401)
    return user
