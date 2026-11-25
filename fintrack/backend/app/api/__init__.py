from .auth import bp as auth_bp
from .docs import bp as docs_bp
from .portfolios import bp as portfolios_bp
from .transactions import bp as transactions_bp


def register_blueprints(app):
    for blueprint in (docs_bp, auth_bp, portfolios_bp, transactions_bp):
        app.register_blueprint(blueprint)
