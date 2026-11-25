"""HTTP API blueprints."""
from .routes.auth import auth_bp
from .routes.portfolios import portfolios_bp
from .routes.summary import summary_bp
from .routes.transactions import transactions_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(portfolios_bp, url_prefix="/api/portfolios")
    app.register_blueprint(transactions_bp, url_prefix="/api")
    app.register_blueprint(summary_bp, url_prefix="/api/summary")
