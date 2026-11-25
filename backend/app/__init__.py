import click
from flask import Flask

from .utils.decorators import _load_local_env

_load_local_env()

from config import Config

from .api import register_blueprints
from .errors import register_error_handlers
from .extensions import cors, db, migrate

INSECURE_DEFAULT_SECRET = "dev-only-change-me"

def create_app(config_object=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    if app.config["APP_ENV"] == "production" and app.config["SECRET_KEY"] == INSECURE_DEFAULT_SECRET:
        raise RuntimeError("SECRET_KEY must be set to a strong random value in production.")

    db.init_app(app)
    from . import models

    migrate.init_app(app, db)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
        allow_headers=["Authorization", "Content-Type"],
    )

    register_blueprints(app)
    register_error_handlers(app)

    @app.after_request
    def security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Cache-Control", "no-store")
        return response

    @app.cli.command("seed-demo")
    def seed_demo_command():
        from .seed import seed_demo

        created = seed_demo()
        click.echo("Demo data created." if created else "Demo data already present.")

    return app
