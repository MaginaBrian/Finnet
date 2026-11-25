from flask import Blueprint

from app.security import login_required
from app.services.portfolio_service import (
    create_portfolio,
    delete_portfolio,
    get_portfolio,
    list_portfolios,
    update_portfolio,
)
from app.services.validation import json_body, validate_portfolio
from app.utils.responses import ok

portfolios_bp = Blueprint("portfolios", __name__)


@portfolios_bp.get("/", strict_slashes=False)
@login_required
def index():
    return ok(list_portfolios())


@portfolios_bp.post("/", strict_slashes=False)
@login_required
def create():
    return ok(create_portfolio(validate_portfolio(json_body())), 201)


@portfolios_bp.get("/<int:portfolio_id>")
@login_required
def show(portfolio_id):
    return ok(get_portfolio(portfolio_id, include_transactions=True))


@portfolios_bp.put("/<int:portfolio_id>")
@login_required
def update(portfolio_id):
    return ok(update_portfolio(portfolio_id, validate_portfolio(json_body())))


@portfolios_bp.delete("/<int:portfolio_id>")
@login_required
def destroy(portfolio_id):
    delete_portfolio(portfolio_id)
    return ok({"deleted": True})
