from flask import Flask
from flask_jwt_extended import JWTManager

from app.config import Config
from app.extensions import cors, db, jwt, migrate
from app.utils.responses import APIError, error


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    from app import models  # noqa: F401
    from app.routes import register_blueprints

    register_blueprints(app)
    _register_handlers(app, jwt)
    return app


def _register_handlers(app, jwt_manager: JWTManager):
    @app.errorhandler(APIError)
    def handle_api_error(err):
        db.session.rollback()
        return error(err.message, err.status)

    @jwt_manager.unauthorized_loader
    def missing_token(_reason):
        return error("Authentication required", 401)

    @jwt_manager.invalid_token_loader
    def invalid_token(_reason):
        return error("Invalid token", 401)

    @jwt_manager.expired_token_loader
    def expired_token(_header, _payload):
        return error("Token expired", 401)
